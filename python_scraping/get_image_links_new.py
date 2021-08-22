#
# Source
#   https://towardsdatascience.com/image-scraping-with-python-a96feda8af2d
#
import io
import os
import time
import requests
import hashlib
from string_utils import asciify
from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def fetch_image_urls(
    query: str,
    max_links_to_fetch: int,
    driver: webdriver,
    output: str,
    sleep_time: float = 0.5
):
    def scroll_to_end(driver):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(sleep_time)

    # build the google query
    search_url = "https://www.google.com/search?safe=off&site=&tbm=isch&source=hp&q={q}&oq={q}&gs_l=img"

    # load the page
    driver.get(search_url.format(q=query))

    image_urls = set()
    thumbnails = []
    while len(image_urls) < max_links_to_fetch:
        print(f"current total images: {len(image_urls)}")
        scroll_to_end(driver)

        last_index = len(thumbnails)

        # get all image thumbnail results
        thumbnails = driver.find_elements_by_css_selector("img.Q4Ludriver")
        total_count = len(thumbnails)

        if last_index < total_count:
            print(f"Loaded more images: {total_count - last_index}")
        else:
            print(f"No more images found")
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
                    persist_image(output, src)
                    print(f"{len(image_urls)} images downloaded")

        load_more_button = driver.find_element_by_css_selector(".mye4qd")
        if load_more_button:
            driver.execute_script("document.querySelector('.mye4qd').click();")
            time.sleep(sleep_time)

    print(f"Downloaded {len(image_urls)} images")
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


def search_and_download(query: str, target_path="./images", count=5):
    output = os.path.join(target_path, "_".join(asciify(query.lower()).split(" ")))

    if not os.path.exists(output):
        os.makedirs(output)

    # See for why options below
    # https://stackoverflow.com/questions/50790733/unknown-error-devtoolsactiveport-file-doesnt-exist-error-while-executing-selen/50791503#50791503
    #
    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.headless = True
    with webdriver.Chrome(options=options) as driver:
        fetch_image_urls(
            query,
            count,
            driver=driver,
            output=output,
            sleep_time=0.5,
        )
