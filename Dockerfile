FROM python:3.12 AS python

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

FROM rust:1.85 AS rust

RUN apt-get update && apt-get install build-essential libssl-dev pkg-config -y && \
    rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt install -y openssl

WORKDIR /certs

COPY --from=python /certs ./

WORKDIR /app

COPY Cargo.toml Cargo.lock ./

COPY src ./src

RUN cargo build --release

CMD ["/app/target/release/rust_client"]

FROM python AS receiver

COPY ./receiver ./receiver

CMD ["python", "-m", "receiver.tcp"]

FROM go AS go_receiver

WORKDIR /app

COPY ./go_receiver ./go_receiver