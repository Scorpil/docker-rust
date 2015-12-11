FROM debian:jessie
MAINTAINER Andrew Scorpil "dev@scorpil.com"

RUN apt-get update && \
    apt-get dist-upgrade -qqy && \
    apt-get install \
    	    build-essential \
	    ca-certificates \
	    curl \
       	    -qqy \
    	    --no-install-recommends \
	    && rm -rf /var/lib/apt/lists/*

ENV DEBIAN_FRONTEND=noninteractive \
    RUST_HOME=/rust \
    RUST_VERSION=1.5.0

ENV RUST_ARCHIVE=rust-$RUST_VERSION-x86_64-unknown-linux-gnu.tar.gz
ENV RUST_DOWNLOAD_URL=https://static.rust-lang.org/dist/$RUST_ARCHIVE \
    RUST_ARCHIVE_SHA256=60b83f74d882ce2ba5bc979b5b0589dca56659f215b3259e7188fed8c50aac9d

ENV PATH=$PATH:$RUST_HOME

RUN mkdir $RUST_HOME
WORKDIR $RUST_HOME

RUN curl -fsSL $RUST_DOWNLOAD_URL -o $RUST_ARCHIVE \
    && echo "$RUST_ARCHIVE_SHA256  $RUST_ARCHIVE" | sha256sum -c - \
    && tar -C $RUST_HOME -xzf $RUST_ARCHIVE --strip-components=1 \
    && rm $RUST_ARCHIVE \
    && ./install.sh
