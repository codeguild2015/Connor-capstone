# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0011_delete_twitter'),
    ]

    operations = [
        migrations.AddField(
            model_name='bar',
            name='twitter',
            field=models.TextField(default=''),
        ),
    ]
