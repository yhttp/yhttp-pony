PY = python3
PIP = pip3
TEST_DIR = tests
PRJ = yhttp.extensions.pony
PYTEST_FLAGS = -v


.PHONY: test
test:
	pytest $(PYTEST_FLAGS) $(TEST_DIR)


.PHONY: cover
cover:
	pytest $(PYTEST_FLAGS) --cov=$(PRJ) $(TEST_DIR)


.PHONY: lint
lint:
	flake8


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
