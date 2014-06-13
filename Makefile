test pyvows:
	@rm -f .coverage*
	@coverage run  --source=tornado_eventsource --branch `which nosetests` -vv -s tests
	@coverage report -m

setup:
	@pip install -Ue.\[tests\]
