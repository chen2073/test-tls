FROM python:3.9 as python

# Install required packages
RUN apt-get update && apt-get install -y \
    openssl \
    && rm -rf /var/lib/apt/lists/*

# Create directory for certificates
WORKDIR /certs

# Generate private key and self-signed certificate
RUN openssl req -x509 -newkey rsa:4096 -keyout /certs/key.pem -out /certs/cert.pem \
    -days 365 -nodes -subj "/C=US/ST=State/L=City/O=Organization/CN=server"

WORKDIR /app

FROM rust:1.85 as rust

RUN apt-get update && apt-get install build-essential libssl-dev pkg-config -y && \
    rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt install -y openssl

WORKDIR /app

COPY Cargo.toml Cargo.lock ./

COPY src ./src

RUN cargo build --release

CMD ["/app/target/release/rust_client"]