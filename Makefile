.PHONY: clean docs test run

run:clean
	python kitch/runserver.py

clean:
	find . -name '*.pyc' -exec rm -f {} +
test:
	python kitch/test/suite_run.py

docs:
	$(MAKE) -C docs html
