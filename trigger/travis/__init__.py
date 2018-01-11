from flask import Blueprint

bp = Blueprint('travis', __name__)

from .resources import Trigger  # noqa  # isort:skip
bp.add_url_rule(
    '/<project>/<trigger_key>/',
    view_func=Trigger.as_view('travis_trigger'),
    methods=['GET', 'POST'])
