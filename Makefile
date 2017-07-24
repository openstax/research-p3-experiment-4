BINDIR = $(PWD)/.state/env/bin

default:
	@echo "Must call a specific subcommand"
	@exit 1

build:
	docker-compose build

	# Mark this state so that the other target will known it has recently been
	# rebuilt.
	mkdir -p .state
	touch .state/docker-build

serve: .state/docker-build
	docker-compose up

initdb:
	psql -h '127.0.0.1' -d postgres -U postgres -c "DROP DATABASE IF EXISTS exp4"
	psql -h '127.0.0.1' -d postgres -U postgres -c "CREATE DATABASE exp4 ENCODING 'UTF8'"
	alembic upgrade head

devServer:
	docker-compose run web npm start

shell:
	docker-compose run web flask shell

purge:
	rm -rf .state
	docker-compose rm --force --all \

test:
	docker-compose run web env -i ENCODING="C.UTF-8" \
															PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin" \
															bin/tests --postgresql-host db $(T) $(TESTARGS)

clean-pyc:
	find . -name '*.pyc' -exec rm {} +
	find . -name '*.pyo' -exec rm {} +
	find . -name '*~' -exec rm {} +
