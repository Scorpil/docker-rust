FROM scorpil/rust:1.6

RUN mkdir -p /rust/app
WORKDIR /rust/app

ONBUILD COPY . /rust/app
ONBUILD RUN cargo build --release

CMD cargo run --release
