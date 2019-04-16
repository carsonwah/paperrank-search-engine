# PaperRank: A Reputation-based Search Engine for Academic Papers

## 1. Getting Started

You may run it locally or inside docker.

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

Run `docker ps` to view your running containers.  
Run `docker logs -f flask_server` to view server logs.  
Run `docker exec -it flask_server bash` to get into the container.  
Go to http://localhost:8000/ to view the UI.

#### Other useful commands

```bash
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
  - Elasticsearch
- **paperrank/**
  - Algorithm of PaperRank
- nginx/
  - Reverse proxy server (for deployment only)
- requirements.txt
  - Python dependencies
