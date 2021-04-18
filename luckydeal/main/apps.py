from django.apps import AppConfig

class MainConfig(AppConfig):
    name = 'main'

    def ready(self):
        from .sheduler import sheduler_start
        sheduler_start()
