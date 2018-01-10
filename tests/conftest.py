import os
import shutil

import pytest

from tests import ApiClient
from trigger import TriggerApp

SPEC_NAME = 'spec.yaml'
SPEC_CONTENT = """
travis:
  secret_key: lolkekmakarek

  repos:
    awesome_repo:
      awesome_trigger_token: awesome%2Fawesome_repo
    yet_another_repo:
      yet_another_trigger_token: awesome%2Fyet_another_repo
"""
SPEC_DICT = {
    'travis': {
        'secret_key': 'lolkekmakarek',
        'repos': {
            'awesome_repo': {
                'awesome_trigger_token': 'awesome%2Fawesome_repo',
            },
            'yet_another_repo': {
                'yet_another_trigger_token': 'awesome%2Fyet_another_repo',
            },
        },
    },
}


@pytest.fixture(scope='session')
def spec_dict() -> dict:
    return SPEC_DICT


@pytest.fixture(scope='session')
def spec(tmpdir_factory) -> str:
    tmpdir = tmpdir_factory.mktemp('trigger')
    spec_path = os.path.join(tmpdir, SPEC_NAME)

    with open(spec_path, 'w') as spec:
        spec.write(SPEC_CONTENT)

    yield spec_path

    shutil.rmtree(tmpdir, ignore_errors=True)


@pytest.fixture(scope='session')
def config(spec) -> dict:
    return dict(
        SPEC_PATH=spec,
    )


@pytest.fixture(scope='session', autouse=True)
def app(config) -> TriggerApp:
    app = TriggerApp('trigger', config=config)
    app.app_context().push()

    app.test_client_class = ApiClient

    return app


@pytest.fixture
def client(app):
    return app.test_client()
