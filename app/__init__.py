from .celery_app import celery_app

__all__ = ['celery_app']

default_app_config = 'app.apps.AppConfig'