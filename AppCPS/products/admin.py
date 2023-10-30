from django.contrib import admin
from .models import product
from .resources import MyModelResource
from import_export.admin import ImportExportModelAdmin
# Register your models here.

class MyModelAdmin(ImportExportModelAdmin):
    resource_class = MyModelResource

admin.site.register(product, MyModelAdmin)