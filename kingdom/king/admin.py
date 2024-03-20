from django.contrib import admin
from .models import King, Kingdom, Servant, TestCase
# Register your models here.
admin.site.register([King, Kingdom, Servant, TestCase])