from django.contrib import admin

# Register your models here.
from app.models import Person
from app.models import Orders
from app.models import Uploads

admin.site.register(Person)
admin.site.register(Orders)
admin.site.register(Uploads)