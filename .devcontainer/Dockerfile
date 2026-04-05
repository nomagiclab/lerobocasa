FROM mcr.microsoft.com/devcontainers/base:ubuntu-24.04

RUN apt-get update \
	&& apt-get install -y --no-install-recommends \
		build-essential \
		python3.12-dev \
		libhidapi-hidraw0 \
		libhidapi-libusb0 \
		libusb-1.0-0 \
	&& rm -rf /var/lib/apt/lists/*

RUN curl -LsSf https://astral.sh/uv/install.sh | env UV_INSTALL_DIR=/usr/local/bin sh

USER vscode

WORKDIR /workspaces/lerobocasa