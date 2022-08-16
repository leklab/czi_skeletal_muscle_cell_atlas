#!/bin/bash
set -eu

export PATH=$PATH:node_modules/.bin

export NODE_ENV="development"

#DEFAULT_ELASTICSEARCH_URL="http://localhost:9200"
#export ELASTICSEARCH_URL=${ELASTICSEARCH_URL:-$DEFAULT_ELASTICSEARCH_URL}

# Server port
export GRAPHQL_PORT=8007

rm -rf dist

# Bundle server once before starting nodemon
webpack --display=errors-only

webpack --display=errors-only --watch &
PID[0]=$!

nodemon dist/server.js &
PID[1]=$!

trap "kill ${PID[0]} ${PID[1]}; exit 1" INT

wait
