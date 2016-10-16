BINDIR = $(PWD)/.state/env/bin

default:
	@echo "Must call a specific subcommand"
	@exit 1

build:
	docker-compose build

	# Mark this state so that the other target will known it's recently been
	# rebuilt.
	mkdir -p .state
	touch .state/docker-build

serve: .state/docker-build
	docker-compose up

initdb:
	docker-compose run web psql -h db -d postgres -U postgres -c "DROP DATABASE IF EXISTS app"
	docker-compose run web psql -h db -d postgres -U postgres -c "DROP DATABASE IF EXISTS test"
	docker-compose run web psql -h db -d postgres -U postgres -c "CREATE DATABASE app ENCODING 'UTF8'"
	docker-compose run web psql -h db -d postgres -U postgres -c "CREATE DATABASE test ENCODING 'UTF8'"
	docker-compose run web alembic upgrade head

devServer:
	docker-compose run web npm start

shell:
	docker-compose run web flask shell

purge:
	rm -rf .state
	docker-compose rm --force --all
