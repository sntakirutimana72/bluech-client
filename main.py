if __name__ == '__main__':
    from src.helpers.logger import Logger

    Logger.setup_logger()
    Logger.info('Starting application')
    Logger.info('Engage startup protocol')

    from src.protocols.startup import routine_001

    routine_001()
    Logger.info('Startup protocol engaged successfully.')

    from src.views.app import BluechClientApp

    BluechClientApp().run()
    Logger.info('Application closed')
