from django.apps import AppConfig

class MainConfig(AppConfig):
    name = 'main'
    verbose_name = 'Основное приложение'

    def ready(self):
        from .sheduler import sheduler_start
        sheduler_start()
