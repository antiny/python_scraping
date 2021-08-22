import typer
from python_scraping.get_image_links_new import search_and_download


app = typer.Typer()


@app.command()
def scrape(query: str, count: int = 1000):
    search_and_download(query, number_images=count)


if __name__ == "__main__":
    app()
