# Generated by Django 3.2.9 on 2021-11-20 04:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_auto_20211118_2156'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='is_available',
            field=models.BooleanField(default=True),
        ),
    ]