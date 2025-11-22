FROM python:3.11-slim-bookworm as build

ENV PIP_DEFAULT_TIMEOUT=100 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    DEBIAN_FRONTEND=noninteractive

WORKDIR /

COPY ./backend/requirements.txt .

# Install system deps needed for HTML→PDF (wkhtmltopdf + fonts + X virtual framebuffer)
# NOTE: Combine update+install, then clean once to avoid apt cache issues.
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        lsb-release \
        software-properties-common \
        xvfb \
        xfonts-100dpi \
        xfonts-75dpi \
        xfonts-scalable \
        wkhtmltopdf && \
    rm -rf /var/lib/apt/lists/*

# Setup env + Python deps (same intent as before)
RUN set -ex \
    && addgroup --system --gid 1001 appgroup \
    && adduser --system --uid 1001 --gid 1001 --no-create-home appuser \
    && apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y --no-install-recommends procps supervisor \
    && pip install uv \
    && uv pip sync requirements.txt --system \
    && apt-get autoremove -y \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/*

# Ensure .temp exists so wkhtmltopdf always works
RUN mkdir -p /base/.temp && chmod 777 /base/.temp
