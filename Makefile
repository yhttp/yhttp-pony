PY = python3
PIP = pip3
TEST_DIR = tests
PRJ = yhttp.ext.pony
PYTEST_FLAGS = -v
HERE = $(shell readlink -f `dirname .`)
VENVNAME = $(shell basename $(HERE) | cut -d'-' -f1)
VENV = $(HOME)/.virtualenvs/$(VENVNAME)


.PHONY: test
test:
	pytest $(PYTEST_FLAGS) $(TEST_DIR)


.PHONY: cover
cover:
	pytest $(PYTEST_FLAGS) --cov=$(PRJ) $(TEST_DIR)


.PHONY: lint
lint:
	flake8


.PHONY: venv
venv:
	python3 -m venv $(VENV)


.PHONY: env
env:
	$(PIP) install -r requirements-dev.txt
	$(PIP) install -e .


.PHONY: sdist
sdist:
	$(PY) setup.py sdist


.PHONY: bdist
bdist:
	$(PY) setup.py bdist_egg


.PHONY: dist
dist: sdist bdist


.PHONY: pypi
pypi: dist
	twine upload dist/*.gz dist/*.egg


.PHONY: clean
clean:
	rm -rf build/*
