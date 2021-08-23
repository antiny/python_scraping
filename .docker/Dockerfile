#
# https://github.com/joyzoursky/docker-python-chromedriver/blob/master/py-debian/3.9/Dockerfile
#
FROM python:3.9

ARG DEBIAN_FRONTEND=noninteractive
ENV LANG=C.UTF-8

# install google chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
RUN apt-get -y update
RUN apt-get install -y google-chrome-stable

# install chromedriver
RUN apt-get install -yqq unzip
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/

# set display port to avoid crash
ENV DISPLAY=:99

WORKDIR /app/

# Install Poetry
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

# TODO: to extract and reduce dependencies
COPY ./pyproject.toml ./poetry.lock* ./
COPY ./python_scraping python_scraping
COPY ./test test

RUN poetry install

ENTRYPOINT [ "poetry", "run", "python", "python_scraping/cli.py", "scrape", "--headless" ]
