from import_export import resources
from .models import Product

class MyModelResource(resources.ModelResource):
    class Meta:
        model = Product