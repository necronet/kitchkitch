.PHONY: clean docs test run print

SUITE = 'all'

run:clean
	python kitch/runserver.py

clean:
	find . -name '*.pyc' -exec rm -f {} +
test:
	python kitch/test/suite_run.py --test $(SUITE)

docs:
	$(MAKE) -C docs html
