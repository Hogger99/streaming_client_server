#!/usr/bin/env bash


docker pull confluentinc/cp-zookeeper:5.4.2
docker pull confluentinc/cp-kafka:5.4.2

docker-compose -f docker-compose.yml up -d