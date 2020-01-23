

.PHONY=cover

cover:
	pytest --cov=yhttp.extensions.pony tests

