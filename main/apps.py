from django.apps import AppConfig


class MainAppConfig(AppConfig):

    name = 'main'
    verbose_name = 'Main'

    def ready(self):

        # import signal handlers
        import main.signals