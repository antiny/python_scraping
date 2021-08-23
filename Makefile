build:
	docker build -f .docker/Dockerfile -t python_scraping .

run_test:
	poetry run python python_scraping/cli.py scrape

run_docker_test:
	./scrape.sh --max-results 12 iphone

run_docker_bash:
	docker run -it --rm --volume "$(pwd)/images:/app/images" --entrypoint /bin/bash python_scraping
