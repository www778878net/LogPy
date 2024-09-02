from invoke import task, run, Program

@task
def build(c):
    run("python -m build")

@task
def install(c):
    run("pip install . --force-reinstall")

@task
def setup(c):
    run("pip install build")
    build(c)
    install(c)

@task
def publish(c):
    build(c)
    run("twine upload --repository pypi dist/*")

@task
def run_all(c):
    setup(c)
    run("pytest")
    publish(c)

if __name__ == "__main__":
    import sys
    program = Program()
    sys.exit(program.run())