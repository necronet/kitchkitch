clean:
	find . -name '*.pyc' -exec rm -f {} +
docs:
	$(MAKE) -C docs html
