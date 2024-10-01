# blog/admin.py
# tell the admin we want to administer these models
from django.contrib import admin

from .models import *
# Register your models here.

# tells the admin to work with Article
admin.site.register(Article)
