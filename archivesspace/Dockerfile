FROM alpine:3.8.4 as builder
WORKDIR /usr/src/app
ARG BRANCH=master
RUN apk update && apk add \
    git \
   && echo "Cloning UTK Local" \
   && git clone --progress https://github.com/utkdigitalinitiatives/utk-archivesspace-local local \
   && cd local \
   && git checkout -b build-app origin/$BRANCH

FROM archivesspace/archivesspace:2.5.2