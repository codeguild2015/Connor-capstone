# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0010_bar_stripped_name'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Twitter',
        ),
    ]
