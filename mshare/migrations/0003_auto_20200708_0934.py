# Generated by Django 3.0.7 on 2020-07-08 04:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mshare', '0002_auto_20200708_0923'),
    ]

    operations = [
        migrations.AlterField(
            model_name='share',
            name='owner',
            field=models.CharField(max_length=30),
        ),
    ]
