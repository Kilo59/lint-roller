init:
ifeq ($(TRAVIS), true)
		pip install pipenv
		pipenv sync --dev
		# coverage doesn't work correctly without this (in travis) ??
		touch tests/__init__.py
else
		pipenv sync --dev
		pre-commit install
endif

test:
	pytest -rf --cov-report term-missing --cov-report xml --cov=lint_roller tests/

lint:
ifeq ($(TRAVIS_PYTHON_VERSION), 3.7)
		pylint -f colorized lint_roller

else
		echo "Only lint for Python3.7"
endif

format:
	black .

check_format:
ifeq ($(TRAVIS_PYTHON_VERSION), 3.7)
		black . --check
else
		echo "Only check format on Python3.7"
endif

pre:
	pre-commit run --all-files
