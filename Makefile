ENV=~/venv/folios

build-env:
	virtualenv -p /usr/bin/python3 --prompt "(folios)" $(ENV)
	. $(ENV)/bin/activate; PIP_DOWNLOAD_CACHE=./.pip_cache pip install -r requirements.txt
	. $(ENV)/bin/activate; python3 setup.py install
remove-env:
	rm -rf $(ENV)
rebuild-env: remove-env build-env

test:
	python3 setup.py test

test-installed:
	@[ -d $(ENV) ] || make build-env
	. $(ENV)/bin/activate; cd /tmp; nosetests3 $(ENV)/lib/python*/site-packages/Folio*/folios/tests

call:
	@[ -d $(ENV) ] || make build-env
	. $(ENV)/bin/activate; cd /tmp; folios $(ARGS)
	

clean: clean-build clean-python
clean-build:
	-rm -rf build
	-rm -rf dist
	-rm -rf Folios.egg-info
clean-python:
	-find . -type d -name __pycache__ -exec rm -rf {} \;
	-find . -type f -name *.pyc -exec rm -rf {} \;
