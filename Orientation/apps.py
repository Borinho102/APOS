from django.apps import AppConfig


class OrientationConfig(AppConfig):
    name = 'Orientation'

    def ready(self):
        import Orientation.signals
