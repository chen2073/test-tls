FROM python:3.9

# Install required packages
RUN apt-get update && apt-get install -y \
    openssl \
    && rm -rf /var/lib/apt/lists/*

# Create directory for certificates
WORKDIR /certs

# Generate private key and self-signed certificate
RUN openssl req -x509 -newkey rsa:4096 -keyout /certs/server.key -out /certs/server.crt \
    -days 365 -nodes -subj "/C=US/ST=State/L=City/O=Organization/CN=localhost"

# Set proper permissions for the private key
RUN chmod 600 /certs/server.key
RUN chmod 644 /certs/server.crt

WORKDIR /app

# Copy the source code
COPY . /app
