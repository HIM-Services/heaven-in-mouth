POSTGRES_CONTIANER_NAME_TEST=postgres_test
POSTGRES_CONTAINER_NAME=heaven-in-mouth-postgres-1
POSTGRES_MOUNT_PATH=/var/tmp/heaven_in_mouth_db_data
FLASK_CONTAINER_NAME=heaven-in-mouth-flask-1
FLASK_CONTAINER_NAME_TEST=flask_test

.PHONY: up
up:
	docker compose up

.PHONY: stop
stop:
	docker compose stop

.PHONY: init
init:
	if [ ! -d $(POSTGRES_MOUNT_PATH) ]; then \
	mkdir $(POSTGRES_MOUNT_PATH); \
	fi

	docker compose up -d

	until docker exec $(POSTGRES_CONTAINER_NAME) pg_isready ; do sleep 5 ; done

	docker exec $(POSTGRES_CONTAINER_NAME) sh -c "psql -U postgres -d heaven_in_mouth < db_setup.sql"

.PHONY: up-b
up-b:
	docker compose up --build

.PHONY: test
test:
	docker compose -f docker-compose-test.yml up -d --build
	until docker exec $(POSTGRES_CONTIANER_NAME_TEST) pg_isready ; do sleep 5 ; done
	docker exec $(FLASK_CONTAINER_NAME_TEST) sh -c "pytest ../tests"
	docker compose -f docker-compose-test.yml down

#.PHONY: lint
#lint:
#	flake8 --append-config tox.ini $(git ls-files "*.py")