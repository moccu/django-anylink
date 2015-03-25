.PHONY: tests coverage coverage-html
APP=anylink/
OPTS=

help:
	@echo "tests - run tests"
	@echo "coverage - run tests with coverage enabled"
	@echo "coverage-html - run tests with coverage html export enabled"

tests:
	py.test ${OPTS} testing/pytests


coverage:
	coverage run `which py.test` ${OPTS} testing/pytests
	coverage report -m --include=${APP}/*


coverage-html:
	coverage run `which py.test` ${OPTS} testing/pytests
	coverage html -d htmlcov --include=${APP}/*
