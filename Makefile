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
	py.test ${OPTS} --cov=${APP} --cov-report=term-missing testing/pytests


coverage-html:
	py.test ${OPTS} --cov=${APP} --cov-report=term-missing --cov-report=html testing/pytests
