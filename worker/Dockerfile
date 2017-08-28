FROM python:latest

LABEL Description="Pipwatch-worker container" Maintainer="Aleksander Gondek" Version="alpha"

ENV PYTHONPATH /pipwatch-worker

WORKDIR /pipwatch-worker
ADD . /pipwatch-worker

RUN pip install -r requirements.txt

CMD ["celery", "worker", "-A=pipwatch_worker.celery.worker:worker",  "-l=debug"]
