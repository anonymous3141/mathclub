# Generated by Django 3.1.7 on 2021-05-13 05:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('db', '0005_auto_20210512_0736'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userproblemverdict',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]