# convenience makefile to boostrap & run buildout
# use `make options=-v` to run buildout with extra options

version = 2.7
python = bin/python
options =

all: docs tests

coverage:
	bin/coverage
	bin/report

htmlcov/index.html: src/pas/plugins/shibboleth/*.py bin/coverage
	@bin/coverage run bin/test
	@bin/coverage html -i
	@touch $@
	@echo "Coverage report was generated at '$@'."

.installed.cfg: bin/buildout buildout.cfg setup.py
	bin/buildout $(options)

bin/buildout: $(python) buildout.cfg bootstrap.py
	$(python) bootstrap.py
	@touch $@

$(python):
	virtualenv -p python$(version) --no-site-packages .
	@touch $@

tests:
	@bin/test
	@bin/code-analysis

clean:
	@rm -rf .coverage .installed.cfg .mr.developer.cfg bin docs/html htmlcov \
		parts develop-eggs src/pas.plugins.shibboleth.egg-info lib include .Python

.PHONY: all coverage docs tests clean
