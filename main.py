if __name__ == '__main__':
    from src.helpers.logger import logging
    logging('Starting application..', 'i')

    from src.protocols.startup import routine_001
    routine_001()  # engaging startup routine

    from src.uix.app import BluechClientApp

    BluechClientApp().run()
