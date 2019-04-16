FROM python:3.6.7

RUN mkdir -p /app/paperrank
WORKDIR /app/paperrank
# COPY . /home/app/paperrank

# Use COPY because volumes are not available during build
COPY ./requirements.txt /app/paperrank
RUN pip install --no-cache-dir -r requirements.txt

ADD . /app/paperrank
