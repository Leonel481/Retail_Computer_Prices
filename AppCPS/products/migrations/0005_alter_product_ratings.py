# Generated by Django 4.2.6 on 2023-11-04 17:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_brand_category_company_alter_product_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='ratings',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
