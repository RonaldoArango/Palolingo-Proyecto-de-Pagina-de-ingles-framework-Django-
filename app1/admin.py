from django.contrib import admin
from .models import *
from .models import Forum

# Register your models here.
admin.site.register(Forum)
admin.site.register(Discussion)