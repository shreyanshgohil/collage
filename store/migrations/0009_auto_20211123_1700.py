# Generated by Django 3.2.9 on 2021-11-23 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0008_auto_20211122_2124'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='color',
            field=models.ManyToManyField(blank=True, to='store.Color'),
        ),
        migrations.AddField(
            model_name='cartitem',
            name='size',
            field=models.ManyToManyField(blank=True, to='store.Size'),
        ),
    ]
