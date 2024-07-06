#! /bin/bash

# Run docker with db initialization steps
docker-compose up -d

DOCKER_CONTAINER_NAME="heaven-in-mouth-postgres-1"
until docker exec $DOCKER_CONTAINER_NAME pg_isready ; do sleep 5 ; done

docker exec $DOCKER_CONTAINER_NAME sh -c "psql -U postgres -d heaven_in_mouth < db_setup.sql"



