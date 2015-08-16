# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import redactor.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('content', redactor.fields.RedactorField(verbose_name='info')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('status', models.SmallIntegerField(default=1, verbose_name=b'Status', choices=[(0, b'Inactive'), (1, b'Active')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
