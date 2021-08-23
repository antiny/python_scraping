#
# Source
#   https://towardsdatascience.com/image-scraping-with-python-a96feda8af2d
#
import io
import os
import time
import requests
import hashlib
from requests.api import head
from string_utils import asciify
from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def fetch_image_urls(
    query: str,
    max_results: int,
    driver: webdriver,
    output_path: str,
    sleep_time: float = 0.5
):
    def scroll_to_end(driver):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(sleep_time)

    print(f"searching with query={query}, max_results={max_results}")

    # build the google query
    search_url = f"https://www.google.com/search?safe=off&site=&tbm=isch&source=hp&q={query}&oq={query}&gs_l=img"
    print(f"searching with url={search_url}")
    driver.get(search_url)

    image_urls = set()
    thumbnails = []
    while len(image_urls) < max_results:
        print(f"total downloaded images: {len(image_urls)}")
        scroll_to_end(driver)

        last_index = len(thumbnails)

        # get all image thumbnail results
        thumbnails = driver.find_elements_by_css_selector("img.Q4LuWd")
        total_count = len(thumbnails)

        if last_index < total_count:
            print(f"loaded more results: {total_count - last_index}")
        else:
            print(f"no more results found")
            break

        for img in thumbnails[last_index:total_count]:
            # try to click every thumbnail such that we can get the real image behind it
            try:
                img.click()
                time.sleep(sleep_time)
            except Exception:
                continue

            # extract image urls
            actual_images = driver.find_elements_by_css_selector("img.n3VNCb")
            for actual_image in actual_images:
                src = actual_image.get_attribute("src")
                if "http" in src and src not in image_urls:
                    image_urls.add(src)
                    persist_image(output_path, src)
                    print(f"{len(image_urls)} images downloaded")
                    if len(image_urls) >= max_results:
                        break

            if len(image_urls) >= max_results:
                break

        load_more_button = driver.find_element_by_css_selector(".mye4qd")
        if load_more_button:
            driver.execute_script("document.querySelector('.mye4qd').click();")
            time.sleep(sleep_time)

    print(f"total downloaded images: {len(image_urls)}")
    return image_urls


def persist_image(folder_path: str, url: str):
    try:
        image_content = requests.get(url).content
        image_file = io.BytesIO(image_content)
        image = Image.open(image_file).convert("RGB")

        image_name = hashlib.sha1(image_content).hexdigest()[:10] + ".jpg"
        file_path = os.path.join(folder_path,image_name)

        with open(file_path, "wb") as f:
            image.save(f, "JPEG", quality=85)

    except Exception as e:
        print(f"error - could not download {url} - {e}")


def run_scrape(query: str, max_results=5, target_path="./images", headless=False):
    output_path = os.path.join(target_path, "_".join(asciify(query.lower()).split(" ")))

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    # See for why options below
    # https://stackoverflow.com/questions/50790733/unknown-error-devtoolsactiveport-file-doesnt-exist-error-while-executing-selen/50791503#50791503
    #
    options = Options()

    if headless:
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.headless = True

    with webdriver.Chrome(options=options) as chrome_driver:
        fetch_image_urls(
            query,
            max_results,
            chrome_driver,
            output_path,
            sleep_time=0.5,
        )
