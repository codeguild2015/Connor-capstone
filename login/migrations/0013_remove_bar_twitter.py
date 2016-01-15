# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0012_bar_twitter'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bar',
            name='twitter',
        ),
    ]
