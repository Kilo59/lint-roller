# -*- coding: utf-8 -*-
"""
lint_roller
~~~~~~~~~~~

Audit linting errors and identify cost savings.
"""
from invoke import Collection, Program  # pylint: disable=import-error
from . import tasks


# pylint: disable=invalid-name
program = Program(namespace=Collection.from_module(tasks), version="18.0a.1")

if __name__ == "__main__":
    print(__doc__)
