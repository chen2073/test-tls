FROM rust:1.85 AS build

RUN apt-get update && apt-get install build-essential libssl-dev pkg-config -y && \
    rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt install -y openssl

WORKDIR /app

COPY Cargo.toml Cargo.lock ./

COPY src ./src

RUN cargo build --release

CMD ["/app/target/release/rust_client"]