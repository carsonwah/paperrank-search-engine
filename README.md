# PaperRank: A Reputation-based Search Engine for Academic Papers

## Getting Started

You may run it locally or inside docker.

### I. Backend only

Install `python3`, `virtualenv`.

```bash
$ virtualenv env -p python3  # Use python 3.6+
$ source env/bin/activate
(env) $ pip install -r requirements.txt
(env) $ python app.py
```

Then, go to http://localhost:8000/ and have a check.

### II. Run with elasticsearch using docker

Install [Docker](https://www.docker.com/get-started).

```bash
# Run in foreground
$ docker-compose up

# Run in background
$ docker-compose up -d

# If config has changed, rebuild the image
$ docker-compose up -d --force-recreate --build <container_name>
```

#### Included services

- **nginx** server listening on :80
- **gunicorn** server listening on :8000
- **elasticsearch** server listening on :9200
