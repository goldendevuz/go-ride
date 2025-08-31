# Use an official Python runtime as a parent image
FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        curl gnupg make gettext nano \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install jprq
RUN curl -fsSL https://jprq.io/install.sh | bash

WORKDIR /usr/src/app

RUN pip install --upgrade pip

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy entrypoint + scripts
COPY entrypoint.sh /usr/src/app/entrypoint.sh
COPY start.sh /usr/src/app/start.sh
RUN chmod +x /usr/src/app/entrypoint.sh /usr/src/app/start.sh

COPY . .

EXPOSE 1026

ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
CMD ["bash", "start.sh"]
