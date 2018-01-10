from dotenv_config import Config

from trigger import TriggerApp

conf_loader = Config()
config = dict(
    ERROR_404_HELP=False,
    SPEC_PATH=conf_loader('SPEC_PATH'),
)

app = TriggerApp(__name__, config=config)
