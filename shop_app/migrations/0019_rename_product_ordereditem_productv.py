# Generated by Django 4.2.1 on 2023-09-20 12:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop_app', '0018_remove_order_productv_remove_order_quantity_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ordereditem',
            old_name='product',
            new_name='productv',
        ),
    ]
