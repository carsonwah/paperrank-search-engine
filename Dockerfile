FROM python:3.6.7

RUN mkdir -p /app/i-care
WORKDIR /app/i-care
# COPY . /home/app/i-care

# Use COPY because volumes are not available during build
COPY ./requirements.txt /app/i-care
RUN pip install --no-cache-dir -r requirements.txt