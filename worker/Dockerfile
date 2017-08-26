FROM python:latest

LABEL Description="Pipwatch-worker container" Maintainer="Aleksander Gondek" Version="alpha"

ENV PYTHONPATH /pipwatch-worker

WORKDIR /pipwatch-worker
ADD . /pipwatch-worker

EXPOSE 8080

RUN pip install -r requirements.txt

CMD ["python", "pipwatch_woker/main.py"]
