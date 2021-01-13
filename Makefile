.PHONY: check
check:
	@echo 'run type check'
	@poetry run mypy
	@echo 'run test'
	@poetry run pytest ./test.py
