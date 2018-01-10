import os
import shutil

import pytest

from trigger import TriggerApp

SPEC_NAME = 'spec.yaml'
SPEC_CONTENT = """
travis:
  secret_key: lolkekmakarek

  repos:
    awesome_repo:
      awesome/awesome_repo: awesome_trigger_token
    yet_another_repo:
      awesome/yet_another_repo: yet_another_trigger_token
"""
SPEC_DICT = {
    'travis': {
        'secret_key': 'lolkekmakarek',
        'repos': {
            'awesome_repo': {
                'awesome/awesome_repo': 'awesome_trigger_token',
            },
            'yet_another_repo': {
                'awesome/yet_another_repo': 'yet_another_trigger_token',
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

    return app
