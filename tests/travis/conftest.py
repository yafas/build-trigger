import pytest
import requests_mock


@pytest.fixture
def travis_repos(spec_dict):
    def repos():
        for confs in spec_dict['travis']['repos'].values():
            for repo in confs.values():
                yield repo
    return repos


@pytest.fixture
def travis_api():

    def callback(request, context):
        headers = request._request.headers
        assert headers['Authorization'] == 'token lolkekmakarek'
        assert headers['Travis-API-Version'] == str(3)
        return {}

    return callback


@pytest.fixture
def mock_travis(travis_api, travis_repos):
    with requests_mock.Mocker() as mocker:
        for repo in travis_repos():
            mocker.post(
                f'https://api.travis-ci.org/repo/{repo}/requests',
                status_code=202,
                json=travis_api)
        yield


@pytest.fixture
def mock_travis_errored(travis_api, travis_repos):
    with requests_mock.Mocker() as mocker:
        for repo in travis_repos():
            mocker.post(
                f'https://api.travis-ci.org/repo/{repo}/requests',
                status_code=400)
        yield
