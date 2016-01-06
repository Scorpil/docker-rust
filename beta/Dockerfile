FROM debian:jessie
MAINTAINER Andrew Scorpil "dev@scorpil.com"

ENV DEBIAN_FRONTEND=noninteractive \
    RUST_HOME=/rust

RUN apt-get update && \
    apt-get install \
       ca-certificates \
       curl \
       -qqy \
       --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

ENV RUST_ARCHIVE=rust-beta-x86_64-unknown-linux-gnu.tar.gz
ENV RUST_DOWNLOAD_URL=https://static.rust-lang.org/dist/$RUST_ARCHIVE

RUN mkdir $RUST_HOME
WORKDIR $RUST_HOME

RUN curl -fsOSL $RUST_DOWNLOAD_URL \
    && curl -s $RUST_DOWNLOAD_URL.sha256 | sha256sum -c - \
    && tar -C $RUST_HOME -xzf $RUST_ARCHIVE --strip-components=1 \
    && rm $RUST_ARCHIVE \
    && ./install.sh
