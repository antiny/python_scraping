# Google Image Scraping

This is a convenient docker image that runs selenium and Chrome to scrape google image search result.

# Install

```
make build
```

# Example
To scrape images for term `iphone`, run

```
./scrape.sh iphone
```
by default, it will download up to ~1000 images within the `./images` directory
