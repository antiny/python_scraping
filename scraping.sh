#!/bin/bash

mkdir images
docker run -it --rm --volume "$(pwd)/images:/app/images" python_scraping $1
