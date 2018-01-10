import requests

from . import bp


class TravisApiError(Exception):
    pass


def repo_url(repo_path: str) -> str:
    return f'https://api.travis-ci.org/repo/{repo_path}/requests'


def travis_headers() -> dict:
    token = bp.spec['secret_key']
    return {
        'Authorization': f'token {token}',
        'Travis-API-Version': str(3),
    }


def trigger_travis(project_path: str):
    response = requests.post(repo_url(project_path), headers=travis_headers())
    if response.status_code != 200:
        raise TravisApiError('Travis errored.')
