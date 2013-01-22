.PHONY: clean docs test

clean:
	find . -name '*.pyc' -exec rm -f {} +
test:
	python kitch/test/suite_run.py

docs:
	$(MAKE) -C docs html