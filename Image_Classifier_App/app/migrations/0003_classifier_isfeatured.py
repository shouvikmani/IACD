# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_classifier'),
    ]

    operations = [
        migrations.AddField(
            model_name='classifier',
            name='isFeatured',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]
