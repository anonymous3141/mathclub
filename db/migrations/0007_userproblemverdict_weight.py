# Generated by Django 3.1.7 on 2021-05-13 06:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0006_auto_20210513_0538'),
    ]

    operations = [
        migrations.AddField(
            model_name='userproblemverdict',
            name='weight',
            field=models.IntegerField(default=1),
        ),
    ]
