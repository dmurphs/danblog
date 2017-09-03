# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import redactor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_auto_20150416_0556'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='content',
            field=redactor.fields.RedactorField(verbose_name=b''),
        ),
    ]
