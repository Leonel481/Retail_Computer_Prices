from import_export import resources
from .models import product

class MyModelResource(resources.ModelResource):
    class Meta:
        model = product