from django.apps import AppConfig
import os

class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'
    def ready(self):
        if not os.environ.get('RUN_MAIN'):
            return
        from .tasks import start_scheduler
        start_scheduler()
