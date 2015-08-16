# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20150416_0422'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='linkpost',
            name='category',
        ),
        migrations.RemoveField(
            model_name='linkpost',
            name='user',
        ),
        migrations.DeleteModel(
            name='LinkPost',
        ),
        migrations.AddField(
            model_name='post',
            name='url',
            field=models.URLField(null=True),
            preserve_default=True,
        ),
    ]
