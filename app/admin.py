from django.contrib import admin

# Register your models here.
# from app.models import Person
from app.models import Items
from app.models import Uploads
from app.models import Orders

# admin.site.register(Person)
admin.site.register(Items)
admin.site.register(Uploads)
admin.site.register(Orders)