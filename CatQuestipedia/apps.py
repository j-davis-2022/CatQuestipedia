from django.apps import AppConfig


class CatquestipediaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'CatQuestipedia'

    # def ready(self):
    #   from CatQuestipedia import signals
