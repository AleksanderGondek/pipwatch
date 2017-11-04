# The general flow of following dockerfile has been heavily based upon
# https://github.com/avatsaev/angular4-docker-example project.

### STAGE 1: Build angular app ###
FROM node:8-alpine as builder
WORKDIR /pipwatch-ui-builder
ADD . /pipwatch-ui-builder
RUN yarn cache clean && yarn install --non-interactive && ./node_modules/.bin/ng build --env=prod

### STAGE 2: Setup ngnix ###
FROM nginx:latest
LABEL Description="Pipwatch-ui container" Maintainer="Aleksander Gondek" Version="alpha"

COPY nginx/default.conf /etc/nginx/conf.d/
# Remove default nginx website
RUN rm -rf /usr/share/nginx/html/*
# From 'builder' stage copy over the artifacts in dist folder to default nginx public folder
COPY --from=builder /pipwatch-ui-builder/dist /usr/share/nginx/html

CMD ["nginx", "-g", "daemon off;"]
