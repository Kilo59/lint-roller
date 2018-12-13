# -*- coding: utf-8 -*-
from invoke import task


@task
def lint(ctx, targets="."):
    print("LINTING!")
    if isinstance(targets, (list, tuple, set)):
        targets = " ".join(targets)
    ctx.run(f"pylint {targets}")


@task
def fmt(ctx):
    print("FORMATTING!")
