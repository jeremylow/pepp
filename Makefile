.PHONY: requirements
requirements:
	pip-compile requirements/requirements.in
	pip-compile requirements/dev.in

env:
	pip install -rU requirements/requirements.txt
	pip install -rU requirements/dev.txt
