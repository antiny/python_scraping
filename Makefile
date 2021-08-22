build:
	docker build -f .docker/Dockerfile -t python_scraping .

run_bash:
	docker run -it --rm --entrypoint /bin/bash python_scraping

