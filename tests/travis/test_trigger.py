import pytest


@pytest.mark.usefixtures('mock_travis')
def test_successful(client):
    got = client.api.get(
        '/travis/awesome_repo/awesome_trigger_token/')

    assert got == {'message': ['"awesome_repo" triggered.']}


def test_incorrect_project(client):
    response = client.api.get(
        '/travis/repo/awesome_trigger_token/', as_response=True)

    assert response.status_code == 400
    assert response.json == {'project': ['This repo is not supported.']}


def test_incorrect_key(client):
    response = client.api.get(
        '/travis/awesome_repo/trigger_token/', as_response=True)

    assert response.status_code == 400
    assert response.json == {'trigger_key': ['Invalid trigger key']}


@pytest.mark.usefixtures('mock_travis_errored')
def test_travis_errored(client):
    response = client.api.get(
        '/travis/awesome_repo/awesome_trigger_token/', as_response=True)

    assert response.status_code == 400
    assert response.json == {'travis': ['Travis errored.']}
