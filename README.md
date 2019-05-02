# PaperRank: A Reputation-based Search Engine for Academic Papers

## 1. Getting Started

You may run it locally or inside docker. **Prefer docker**.

### A. Web server only

Install `python3`, `virtualenv`.

```bash
$ virtualenv env -p python3  # Use python 3.6+
$ source env/bin/activate
(env) $ pip install -r requirements.txt
(env) $ python app.py
```

Then, go to http://localhost:8000/ and have a check.

### B. Run server + elasticsearch using docker

Install [Docker](https://www.docker.com/get-started).

```bash
# Run in foreground
$ docker-compose up

# Run in background
$ docker-compose up -d
```

This will boot up the following services

- **nginx** server listening on :80
- **flask** server listening on :8000
- **elasticsearch** server listening on :9200

Go to http://localhost:8000/ to view the UI.

#### Other useful commands

```bash
# View your running containers
$ docker ps

# Shut down all containers
$ docker-compose down

# View server logs
$ docker logs -f flask_server

# Get into the container
$ docker exec -it flask_server bash

# Restart containers
$ docker-compose restart flask_server nginx

# If Dockerfile has changed, rebuild the image
$ docker-compose up -d --force-recreate --build flask_server nginx
```

## 2. Project Structure

- **webapp/**
  - HTTP server serving the search webpages
- **data/**
  - Papers Data
  - Data preprocessing
  - Elasticsearch scripts
- **paperrank/**
  - Algorithm of PaperRank
- nginx/
  - Reverse proxy server (for deployment only)
- requirements.txt
  - Python dependencies

## 3. Usage

### Elasticsearch

Firstly, make sure elasticsearch cluster is up and running.

```bash
cd data/

# Load initial data into elasticsearch
python load.py

# Sample query
python query.py
```

### PaperRank

```bash
# Preprocess data into link csv file
cd paperrank/data/
python preprocess.py
```
