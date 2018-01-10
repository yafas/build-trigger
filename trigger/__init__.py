import importlib

import yaml
from flask import Blueprint, Flask


class TriggerApp(Flask):

    blueprint_module_names = (
    )

    def __init__(self, import_name: str, config: dict, *args, **kwargs):
        super().__init__(import_name, *args, **kwargs)

        self.config.update(config)

        self.load_spec()

        self.init_blueprints()

    def load_spec(self):
        spec_path = self.config['SPEC_PATH']
        with open(spec_path, 'r') as spec:
            self.spec = yaml.load(spec)

    def init_blueprints(self):
        for bp_name in self.blueprint_module_names:
            self.register_blueprint(
                self._import_blueprint(bp_name),
                url_prefix=f'/bp_name')

    def _import_blueprint(self, bp_module_name: str) -> Blueprint:
        bp_module = importlib.import_module(f'{__name__}.{bp_module_name}')
        return bp_module.bp
