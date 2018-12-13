from invoke import task


@task
def lint(ctx):
    print("LINTING!")


@task
def fmt(ctx):
    print("FORMATTING!")
