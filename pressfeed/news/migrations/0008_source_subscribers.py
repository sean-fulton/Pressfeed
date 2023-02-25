# Generated by Django 4.1.4 on 2023-02-23 19:50

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('news', '0007_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='source',
            name='subscribers',
            field=models.ManyToManyField(related_name='sources', to=settings.AUTH_USER_MODEL),
        ),
    ]
