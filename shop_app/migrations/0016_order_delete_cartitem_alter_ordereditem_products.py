# Generated by Django 4.2.1 on 2023-09-18 14:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('shop_app', '0015_alter_product_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1)),
                ('completed', models.BooleanField(default=False)),
                ('productv', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop_app.productvariation')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='CartItem',
        ),
        migrations.AlterField(
            model_name='ordereditem',
            name='products',
            field=models.ManyToManyField(to='shop_app.order'),
        ),
    ]