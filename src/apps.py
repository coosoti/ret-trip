from django.apps import AppConfig


class SrcConfig(AppConfig):
    name = 'src'

    def ready(self):
        import src.signals
