from invoke import task, run
import os
import sys

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
    # 设置 PYTHONPATH 环境变量
    os.environ['PYTHONPATH'] = os.path.abspath(os.path.join(os.path.dirname(__file__), 'src'))
    print("Python 路径:", os.environ['PYTHONPATH'])
    run("pytest")
    publish(c)

if __name__ == "__main__":
    import sys
    program = Program(namespace=Collection(build, install, setup, publish, run_all))
    sys.exit(program.run())