# Use an official Python runtime as a parent image
FROM python:3.13-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies, including gettext and nano
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        curl \
        gnupg \
        make \
        gettext \
        nano \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install jprq (no sudo needed, run as root)
RUN curl -fsSL https://jprq.io/install.sh | bash

# Set the working directory in the container
WORKDIR /usr/src/app

# Upgrade pip to the latest version
RUN pip install --upgrade pip

# Install Python dependencies from requirements.txt
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the application port
EXPOSE 1026

# Run the startup script
CMD ["bash", "start.sh"]
