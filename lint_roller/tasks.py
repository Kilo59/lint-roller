# -*- coding: utf-8 -*-
"""
tasks
~~~~~
Invoke `tasks` file
"""
from typing import Union, List, Tuple, Set
from invoke import task  # pylint: disable=import-error


@task
def lint(context, targets="."):
    """[summary]

    Parameters
    ----------
    context : [type]
        [description]
    targets : Union[str, List, Tuple, Set], optional
        [description] (the default is ".", which [default_description])
    """
    if isinstance(targets, (list, tuple, set)):
        targets = " ".join(targets)
    cmd_result = context.run(f"pylint {targets}")


@task
def fmt(context):
    """[summary]

    Parameters
    ----------
    ctx : [type]
        [description]
    """
    print("FORMATTING!")
