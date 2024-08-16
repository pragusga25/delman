test:
	coverage run --rcfile=.coveragerc -m unittest discover tests

coverage:
	coverage report --rcfile=.coveragerc -m --include="app/services/*,app/routes/*"

coverage-html:
	coverage html --rcfile=.coveragerc --include="app/services/*,app/routes/*"
