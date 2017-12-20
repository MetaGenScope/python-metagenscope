.PHONY: lint

lint:
	pylint --rcfile=.pylintrc metagenscope_cli -f parseable -r n && \
	pycodestyle metagenscope_cli --max-line-length=120 && \
	pydocstyle metagenscope_cli
