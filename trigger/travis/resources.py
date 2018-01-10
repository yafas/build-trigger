from flask.views import MethodView

from . import bp
from .api import TravisApiError, trigger_travis
from .schemas import TravisProjectSchema


@bp.errorhandler(TravisApiError)
def handle_travis_error(error):
    return {'travis': [str(error)]}, 400


class Trigger(MethodView):

    def get(self, **kwargs):
        project_path, errors = TravisProjectSchema().load(kwargs)
        if errors:
            return errors, 400

        trigger_travis(project_path)
        return {'message': ['"awesome_repo" triggered.']}, 200
