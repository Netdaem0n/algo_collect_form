#!/usr/bin/env bash

echo 'Building and running the docker container'
docker build -t my_flask_app .
echo 'Run container'
docker run -d -p 5432:5432 --restart always my_flask_app