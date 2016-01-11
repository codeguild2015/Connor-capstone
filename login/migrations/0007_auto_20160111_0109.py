# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0006_auto_20160111_0109'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bar',
            old_name='gooogle_id',
            new_name='google_id',
        ),
    ]
