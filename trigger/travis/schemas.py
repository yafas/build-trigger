from marshmallow import Schema, ValidationError, fields, post_load, validates

from . import bp


class TravisProjectSchema(Schema):
    project = fields.String(required=True)
    trigger_key = fields.String(required=True)

    @validates('project')
    def validate_project(self, value) -> bool:
        if value not in bp.spec['repos']:
            raise ValidationError('This repo is not supported.')
        return True

    @post_load
    def find_travis_repository(self, data) -> str:
        project_spec = bp.spec['repos'][data['project']]

        try:
            return project_spec[data['trigger_key']]
        except KeyError:
            raise ValidationError('Invalid trigger key', 'trigger_key')
