# -*- coding: utf-8 -*-
"""
lint_roller
~~~~~~~~~~~

Audit linting errors and identify cost savings.
"""
from invoke import Collection, Program
from lint_roller import tasks

program = Program(namespace=Collection.from_module(tasks), version="18.0a.1")

if __name__ == "__main__":
    print(__doc__)
