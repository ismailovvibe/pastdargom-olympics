from django.apps import AppConfig


class OlympiadsConfig(AppConfig):
    name = 'olympiads'

    def ready(self):
        # register signal handlers
        import olympiads.signals  # noqa
