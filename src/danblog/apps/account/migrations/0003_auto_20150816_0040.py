# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_auto_20150416_0422'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bloguser',
            name='summary',
            field=models.TextField(null=True),
        ),
    ]
