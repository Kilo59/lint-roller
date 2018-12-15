# -*- coding: utf-8 -*-
"""
tasks
~~~~~
Invoke `tasks` file
"""
from typing import Union, List, Tuple, Set
from invoke import task  # pylint: disable=import-error


@task
def lint(ctx, targets: Union[str, List, Tuple, Set] = "."):
    """[summary]

    Parameters
    ----------
    ctx : [type]
        [description]
    targets : Union[str, List, Tuple, Set], optional
        [description] (the default is ".", which [default_description])
    """
    print("LINTING!")
    if isinstance(targets, (list, tuple, set)):
        targets = " ".join(targets)
    cmd_result = ctx.run(f"pylint {targets}")


@task
def fmt(ctx):
    """[summary]

    Parameters
    ----------
    ctx : [type]
        [description]
    """
    print("FORMATTING!")
