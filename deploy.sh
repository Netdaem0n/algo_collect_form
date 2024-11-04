#!/usr/bin/env bash

echo 'Building and running the docker container'
docker-compose up --build -d
echo 'Run container'
docker run -d -p 5432:5432 --restart always my_flask_app