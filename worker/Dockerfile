FROM python:latest

LABEL Description="Pipwatch-worker container" Maintainer="Aleksander Gondek" Version="alpha"

ENV PYTHONPATH /pipwatch-worker

WORKDIR /pipwatch-worker

ADD . /pipwatch-worker
ADD ./config-for-docker.ini /pipwatch-worker/config-override.ini

RUN pip install dumb-init
RUN pip install -r requirements.txt

ENTRYPOINT ["dumb-init", "--"]

CMD ["celery", "worker", "-A=pipwatch_worker.celery_components.application:app",  "-l=debug"]
