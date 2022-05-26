from django.contrib import admin

# Register your models here.
from app.models import Person
from app.models import ItemsBestQ
from app.models import UploadsBestQ

admin.site.register(Person)
admin.site.register(ItemsBestQ)
admin.site.register(UploadsBestQ)