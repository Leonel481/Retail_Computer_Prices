from django.contrib import admin
from .models import *
from .resources import MyModelResource
from import_export.admin import ImportExportModelAdmin
# Register your models here.

class MyModelAdmin(ImportExportModelAdmin):
    resource_class = MyModelResource

admin.site.register(Codes, MyModelAdmin)
admin.site.register(Product, MyModelAdmin)
admin.site.register(Brand, MyModelAdmin)
admin.site.register(Category, MyModelAdmin)
admin.site.register(Company, MyModelAdmin)
admin.site.register(Comment, MyModelAdmin)