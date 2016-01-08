FROM scorpil/rust:beta

RUN mkdir -p /rust/app
WORKDIR /rust/app

ONBUILD COPY . /rust/app
ONBUILD RUN cargo build --release

CMD cargo run --release
