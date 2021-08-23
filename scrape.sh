#!/bin/bash

docker run -it --rm --volume "$(pwd)/images:/app/images" python_scraping "$1"
