FROM python:latest

LABEL Description="Pipwatch-api container" Maintainer="Aleksander Gondek" Version="alpha"

ENV PYTHONPATH /pipwatch-api

WORKDIR /pipwatch-api
ADD . /pipwatch-api

EXPOSE 8080

RUN pip install -r requirements.txt

CMD ["python", "pipwatch_api/main.py"]
