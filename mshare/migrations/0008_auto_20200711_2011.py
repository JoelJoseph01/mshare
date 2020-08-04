# Generated by Django 3.0.7 on 2020-07-11 14:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mshare', '0007_auto_20200711_1109'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='like',
            name='post',
        ),
        migrations.RemoveField(
            model_name='like',
            name='user',
        ),
        migrations.RemoveField(
            model_name='like',
            name='value',
        ),
        migrations.AddField(
            model_name='like',
            name='current_item',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='contents', to='mshare.Share'),
        ),
        migrations.AddField(
            model_name='like',
            name='users',
            field=models.ManyToManyField(blank=True, null=True, to=settings.AUTH_USER_MODEL),
        ),
        migrations.RemoveField(
            model_name='share',
            name='likes',
        ),
        migrations.AddField(
            model_name='share',
            name='likes',
            field=models.IntegerField(default=0),
        ),
    ]