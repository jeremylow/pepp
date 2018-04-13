help:
	@echo "build           build dist files"
	@echo "clean           clean up working directory"
	@echo "envi            install requirements"
	@echo "requirements    compile requirements"
	@echo "test            run tests"
	@echo "upload          upload to pypi"

.PHONY: requirements
requirements:
	pip-compile requirements/requirements.in
	pip-compile requirements/dev.in
	pip-compile requirements/local.in

env:
	pip install -Ur requirements/requirements.txt
	pip install -Ur requirements/dev.txt
	pip install -Ur requirements/local.txt

test:
	pytest -s --cov

clean:
	rm -fr build
	rm -fr dist
	find . -name '*.pyc' -exec rm -f {} \;
	find . -name '*.pyo' -exec rm -f {} \;
	find . -name '*~' ! -name '*.un~' -exec rm -f {} \;

build: clean
	python setup.py check
	python setup.py sdist
	python setup.py bdist_wheel

upload: clean build
	twine upload pypi dist/*
