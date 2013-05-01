.PHONY: clean docs test run print install-db deploy

SUITE = 'all'

install-db:
	mysql -u root -p kitch < kitch/schema.sql
	mysql -u root -p kitch_test < kitch/schema.sql

run:clean
	python kitch/runserver.py

clean:
	find . -name 'kitch/*.pyc' -exec rm -f {} +
test:
	python kitch/test/suite_run.py --test $(SUITE)

deploy:
	git push production
