help:
	@echo "requirements    compile requirements"
	@echo "envi            install requirements"
	@echo "test            run tests"
	@echo "clean           clean up working directory"

.PHONY: requirements
requirements:
	pip-compile requirements/requirements.in
	pip-compile requirements/dev.in

env:
	pip install -rU requirements/requirements.txt
	pip install -rU requirements/dev.txt

test:
	pytest --cov

clean:
	rm -fr build
	rm -fr dist
	find . -name '*.pyc' -exec rm -f {} \;
	find . -name '*.pyo' -exec rm -f {} \;
	find . -name '*~' ! -name '*.un~' -exec rm -f {} \;
