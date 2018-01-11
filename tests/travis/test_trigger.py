import pytest


@pytest.mark.parametrize('method', [
    'get',
    'post',
])
@pytest.mark.usefixtures('mock_travis')
def test_successful(method, client):
    got = getattr(client.api, method)(
        '/travis/awesome_repo/awesome_trigger_token/')

    assert got == {'message': ['"awesome_repo" triggered.']}


@pytest.mark.parametrize('method', [
    'get',
    'post',
])
def test_incorrect_project(method, client):
    response = getattr(client.api, method)(
        '/travis/repo/awesome_trigger_token/', as_response=True)

    assert response.status_code == 400
    assert response.json == {'project': ['This repo is not supported.']}


@pytest.mark.parametrize('method', [
    'get',
    'post',
])
def test_incorrect_key(method, client):
    response = getattr(client.api, method)(
        '/travis/awesome_repo/trigger_token/', as_response=True)

    assert response.status_code == 400
    assert response.json == {'trigger_key': ['Invalid trigger key']}


@pytest.mark.parametrize('method', [
    'get',
    'post',
])
@pytest.mark.usefixtures('mock_travis_errored')
def test_travis_errored(method, client):
    response = getattr(client.api, method)(
        '/travis/awesome_repo/awesome_trigger_token/', as_response=True)

    assert response.status_code == 400
    assert response.json == {'travis': ['Travis errored.']}
