# Generated by Django 4.2.1 on 2023-10-26 09:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop_app', '0020_alter_order_user_alter_ordereditem_order'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='orderedItem',
            new_name='OrderItem',
        ),
    ]
