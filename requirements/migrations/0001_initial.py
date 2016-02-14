# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-14 19:06
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Iteration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128)),
                ('description', models.CharField(blank=True, default='', max_length=1024)),
                ('last_updated', models.DateTimeField(auto_now=True, null=True)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128)),
                ('description', models.CharField(blank=True, default='', max_length=1024)),
                ('last_updated', models.DateTimeField(auto_now=True, null=True)),
            ],
            options={
                'permissions': (('own_project', 'Can own and create projects'),),
            },
        ),
        migrations.CreateModel(
            name='ProjectFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('file', models.FileField(upload_to='project_files')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='requirements.Project')),
            ],
        ),
        migrations.CreateModel(
            name='Story',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128)),
                ('description', models.CharField(blank=True, default='', max_length=1024)),
                ('last_updated', models.DateTimeField(auto_now=True, null=True)),
                ('reason', models.CharField(blank=True, default='', max_length=1024)),
                ('test', models.CharField(blank=True, default='', max_length=1024)),
                ('hours', models.IntegerField(default=0)),
                ('status', models.IntegerField(choices=[(1, 'Unstarted'), (2, 'Started'), (3, 'Completed'), (4, 'Accepted')], default=1)),
                ('points', models.IntegerField(choices=[(0, '0 Not Scaled'), (1, '1 Point'), (2, '2 Points'), (3, '3 Points'), (4, '4 Points'), (5, '5 Points')], default=0)),
                ('pause', models.BooleanField(default=False)),
                ('iteration', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='requirements.Iteration')),
                ('owner', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='requirements.Project')),
            ],
        ),
        migrations.CreateModel(
            name='StoryComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='', max_length=1024)),
                ('comment', models.CharField(default='', max_length=1024)),
                ('last_updated', models.DateTimeField(auto_now=True, null=True)),
                ('story', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='requirements.Story')),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(default='', max_length=1024)),
                ('story', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='requirements.Story')),
            ],
        ),
        migrations.CreateModel(
            name='UserAssociation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(max_length=128)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='requirements.Project')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='project',
            name='users',
            field=models.ManyToManyField(through='requirements.UserAssociation', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='iteration',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='requirements.Project'),
        ),
    ]