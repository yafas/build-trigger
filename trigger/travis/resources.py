from flask import request
from flask.views import View

from . import bp
from .api import TravisApiError, trigger_travis
from .schemas import TravisProjectSchema, ValidationError


@bp.errorhandler(TravisApiError)
def handle_travis_error(error):
    return {'travis': [str(error)]}, 400


@bp.errorhandler(ValidationError)
def handle_schema_validation(error):
    return error.messages, 400


class Trigger(View):

    @staticmethod
    def status_code():
        return 200 if request.method == 'GET' else 201

    def dispatch_request(self, **kwargs):
        project_path, _ = TravisProjectSchema(strict=True).load(kwargs)

        trigger_travis(project_path)

        return {'message': ['"awesome_repo" triggered.']}, self.status_code()
