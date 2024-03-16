"""Celery configuration for user_app."""

import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "user_app.settings")
app = Celery("user_app")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
