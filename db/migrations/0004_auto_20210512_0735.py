# Generated by Django 3.1.7 on 2021-05-12 07:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('db', '0003_auto_20210318_0745'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProblemVerdict',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('response', models.CharField(default='', max_length=100)),
                ('verdict', models.CharField(default='', max_length=20)),
            ],
        ),
        migrations.RemoveField(
            model_name='choice',
            name='question',
        ),
        migrations.DeleteModel(
            name='Forum',
        ),
        migrations.RemoveField(
            model_name='forumpost',
            name='user',
        ),
        migrations.RemoveField(
            model_name='question',
            name='quiz',
        ),
        migrations.AddField(
            model_name='profile',
            name='rating',
            field=models.IntegerField(default=500),
        ),
        migrations.AddField(
            model_name='quiz',
            name='questionList',
            field=models.ManyToManyField(to='db.Question'),
        ),
        migrations.AddField(
            model_name='quiz',
            name='quizResources',
            field=models.CharField(default='', max_length=250),
        ),
        migrations.DeleteModel(
            name='Choice',
        ),
        migrations.DeleteModel(
            name='ForumPost',
        ),
        migrations.AddField(
            model_name='userproblemverdict',
            name='problem',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='db.question'),
        ),
        migrations.AddField(
            model_name='userproblemverdict',
            name='quizDoneIn',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='db.quiz'),
        ),
        migrations.AddField(
            model_name='userproblemverdict',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]