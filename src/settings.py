import pathlib as plib

BASE_DIR = plib.Path(__file__).parent.parent

DYNAMIC_IMPORTS = {
    'app.uix': 'bluech_client.protocols.startup.uix'
}

KV_TEMPLATES_DIR = BASE_DIR / 'src' / 'templates' / 'kv'

STATIC_PATH = BASE_DIR / 'src' / 'static'

COMMON_KV_TEMPLATES = (
    'commons',
)
