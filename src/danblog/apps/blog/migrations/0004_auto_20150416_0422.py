# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0003_post_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='LinkPost',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('status', models.SmallIntegerField(default=1, verbose_name=b'Status', choices=[(0, b'Inactive'), (1, b'Active')])),
                ('name', models.CharField(max_length=255)),
                ('likes', models.IntegerField()),
                ('url', models.URLField()),
                ('category', models.ManyToManyField(to='blog.PostCategory')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='post',
            name='likes',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
