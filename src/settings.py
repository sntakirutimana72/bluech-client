import pathlib as plib

BASE_DIR = plib.Path(__file__).parent.parent

DYNAMIC_IMPORTS = {
    'app.uix': 'bluech_client.protocols.startup.uix'
}
