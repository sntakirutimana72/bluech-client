from ..utils.require import require

uix_module = require('app.uix', ['src', 'protocols'])
configure_framework_logging_system = uix_module.configure_framework_logging_system
configure_app_window_on_startup = uix_module.configure_app_window_on_startup
configure_system_source_for_compiled_version = uix_module.configure_system_source_for_compiled_version

del uix_module
