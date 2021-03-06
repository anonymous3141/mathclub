# Generated by Django 3.1.7 on 2021-03-18 06:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('db', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Forum',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=200)),
                ('archived', models.BooleanField(default=False)),
                ('visibility', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(verbose_name='date published')),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=500)),
                ('visible', models.BooleanField(default=False)),
                ('readOnly', models.BooleanField(default=False)),
            ],
        ),
        migrations.RemoveField(
            model_name='question',
            name='pub_date',
        ),
        migrations.RemoveField(
            model_name='question',
            name='question_text',
        ),
        migrations.AddField(
            model_name='question',
            name='answerType',
            field=models.CharField(choices=[('mc', 'multichoice'), ('ia', '0 to 999 answer')], default='ia', max_length=2),
        ),
        migrations.AddField(
            model_name='question',
            name='correctAnswer',
            field=models.CharField(default='', max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='question',
            name='inUse',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='question',
            name='options',
            field=models.CharField(default='', max_length=500),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='question',
            name='questionHTML',
            field=models.CharField(default='', max_length=1500),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('personal_message', models.CharField(max_length=100)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ForumPost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('postHTML', models.CharField(max_length=3000)),
                ('date', models.DateTimeField(verbose_name='date posted')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='question',
            name='quiz',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='db.quiz'),
            preserve_default=False,
        ),
    ]
