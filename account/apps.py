from django.apps import AppConfig


class AccountConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'account'
    
    def ready(self):
        """
        This method is necessary to activate the 
        signal that I wrote in the signal file here
        """
        from . import signals
