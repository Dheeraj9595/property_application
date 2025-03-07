from django.contrib import admin

from app1.models import Owner, Property

# Register your models here.
admin.site.register([Property, Owner])
