CUR_TAG = $(shell git describe --abbrev=0 --tags 2>/dev/null || (echo '0.0.0') )
TAG_LIST = $(subst ., , $(CUR_TAG))
MAJOR = $(word 1, $(TAG_LIST))
MINOR = $(word 2, $(TAG_LIST))
REV = $(word 3, $(TAG_LIST))

all:

clean:
	rm -rf build dist *egg-info*

.PHONY: upload
upload: test
	python setup.py sdist upload -r pypi

test:
	tox
