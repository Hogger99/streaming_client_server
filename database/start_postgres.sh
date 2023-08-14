#!/usr/bin/env bash

CWD=$(pwd)
export PG_HOME=$(dirname ${CWD})/pg
mkdir -p ${PG_HOME}
echo "PG_HOME=${PG_HOME}"

docker pull postgres

docker-compose -f docker-compose.yml up -d