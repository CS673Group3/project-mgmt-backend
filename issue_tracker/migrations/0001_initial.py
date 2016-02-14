# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-14 19:06
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('requirements', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Issue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField(max_length=2000)),
                ('issue_type', models.CharField(choices=[('Bug', 'Bug'), ('Feature', 'Feature Request'), ('Internal Cleanup', 'Internal Cleanup')], max_length=20)),
                ('status', models.CharField(choices=[('Open-New', 'New'), ('Open-Assigned', 'Assigned'), ('Open-Accepted', 'Accepted'), ('Closed-Fixed', 'Fixed'), ('Closed-Verified', 'Verified'), ('Closed-Working as Intended', 'Working as Intended'), ('Closed-Obsolete', 'Obsolete'), ('Closed-Duplicate', 'Duplicate')], default='new', max_length=20)),
                ('priority', models.CharField(choices=[('High', 'High'), ('Medium', 'Medium'), ('Low', 'Low')], max_length=20)),
                ('submitted_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('closed_date', models.DateTimeField(editable=False, null=True)),
                ('assignee', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='assignee', to=settings.AUTH_USER_MODEL)),
                ('project', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='requirements.Project')),
                ('reporter', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reporter', to=settings.AUTH_USER_MODEL)),
                ('verifier', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='verifier', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='IssueComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField(max_length=2000)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('is_comment', models.BooleanField(default=True)),
                ('issue_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='issue_tracker.Issue')),
                ('poster', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
