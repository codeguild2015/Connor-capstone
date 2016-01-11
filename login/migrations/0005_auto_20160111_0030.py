# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0004_auto_20160111_0029'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bar',
            name='creation_date',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='bar',
            name='updated_date',
            field=models.DateTimeField(null=True),
        ),
    ]
