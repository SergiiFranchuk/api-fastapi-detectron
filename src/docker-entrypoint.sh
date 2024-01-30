#!/bin/bash

while !</dev/tcp/detectron_db/5432;
do
    echo waiting for Postgres to start...;
    sleep 3;
done;

aerich upgrade

uvicorn application.main:application --host 0.0.0.0 --port 8000 --reload