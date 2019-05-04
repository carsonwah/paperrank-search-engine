# PaperRank: A Reputation-based Search Engine for Academic Papers

## 1. Project Structure

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

## 2. Prepare environment

### A. Python virtual environment (Development use)

Install `python3`, `virtualenv`.

```bash
$ virtualenv env -p python3  # "-p python3" means using python 3, needed if you have python 2 as global default
$ source env/bin/activate  # Get into the virtual env
(env) $ pip install -r requirements.txt  # Install dependencies

# Now we can try running some commands
(env) $ python app.py
```

### B. Docker (Start server & elasticsearch)

Install [Docker](https://www.docker.com/get-started).

Then, start docker containers:

```bash
$ docker-compose up -d  # -d means run in background
```

This will boot up the following services:

- **nginx** server listening on :80
- **flask** server listening on :8000
- **elasticsearch** server listening on :9200
- **dejavu** listening on :1358

## 3. Prepare our database

Here are the instructions on how to setup the whole system.

### Download Data

First, prepare the data we need. Since it's too large, we need to download it separately.

Data structure: https://api.semanticscholar.org/corpus/

Removed papers **without valid "outCitations" or valid "inCitations"**.  
Original: 7.35GB, 3000000 papers  
Now: 2.07GB, 425876 papers

1. Download [here](https://drive.google.com/open?id=1VvaRUU4qhq_LE3723G3__O1Fap51b1D_) and unzip.
2. Then, put it in `/data/local/filtered_papers.json`.

### PaperRank

Then, run the PageRank algorithm to compute the scores for ranking.

```bash
# Preprocess data into graph (as a csv file)
cd paperrank/data/
python preprocess.py

# Run PageRank algo and output result to data/pagerank_result.json
cd paperrank/
python PageRank.py
```

### Elasticsearch

Run our elasticsearch cluster and import data into it.

```bash
cd data/

# Load initial data into elasticsearch
python load.py

# Sample query
python query.py
```

### Dajavu

You can look into elasticsearch data easily with dejavu. Go to http://localhost:1358/. Connect it to ES cluster at `http://localhost:9200`.

### Run web UI

Go to http://localhost:8000/ to visit the web UI.


## 4. Other useful commands

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
