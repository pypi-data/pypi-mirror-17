# coding: utf-8
from django.conf import settings
from django.contrib import admin
from . import models

if settings.DEBUG:
    admin.site.register(models.Func)
