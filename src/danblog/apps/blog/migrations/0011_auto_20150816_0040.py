# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import redactor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0010_auto_20150815_2230'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='content',
            field=redactor.fields.RedactorField(verbose_name=b''),
        ),
    ]
