FROM python:latest

LABEL Description="Pipwatch-api container" Maintainer="Aleksander Gondek" Version="alpha"

ENV PYTHONPATH /pipwatch-api

WORKDIR /pipwatch-api
ADD . /pipwatch-api
ADD ./config-for-docker.ini /pipwatch-api/config-override.ini

EXPOSE 8081

RUN pip install dumb-init
RUN pip install -r requirements.txt

ENTRYPOINT ["dumb-init", "--"]

CMD ["python", "pipwatch_api/main.py"]
