import typer
from python_scraping.get_image_links_new import run_scrape


app = typer.Typer()


@app.command()
def about():
    typer.echo("A simple scraping tool")


@app.command()
def scrape(
    query: str,
    max_results: int = 1000,
    headless: bool = typer.Option(False)
    ):
    run_scrape(query, max_results, headless=headless)


if __name__ == "__main__":
    app()
