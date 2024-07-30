from django.apps import AppConfig


class BoardConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'board'

class YourAppConfig(AppConfig):
    name = 'your_app'

    def ready(self):
        import your_app.signals