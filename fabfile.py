from fabric.api import local


def server():
    local('python server')


def client():
    local('python client')


def test():
    local('pytest --cov-report term-missing --cov server')


def notebook():
    local('jupyter notebook')


def kill():
    local('lsof -t -i tcp:8000 | xargs kill')