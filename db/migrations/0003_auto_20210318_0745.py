# Generated by Django 3.1.7 on 2021-03-18 07:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0002_auto_20210318_0657'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='options',
            field=models.CharField(default='', max_length=500),
        ),
    ]
