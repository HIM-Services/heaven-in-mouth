up:
	docker compose up -d

stop:
	docker compose stop

init:
	if [ ! -d /var/tmp/heaven_in_mouth_db_data ]; then \
	mkdir /var/tmp/heaven_in_mouth_db_data; \
	fi

	docker compose up -d

	until docker exec heaven-in-mouth-postgres-1 pg_isready ; do sleep 5 ; done

	docker exec heaven-in-mouth-postgres-1 sh -c "psql -U postgres -d heaven_in_mouth < db_setup.sql"

up-b:
	docker compose up --build -d
