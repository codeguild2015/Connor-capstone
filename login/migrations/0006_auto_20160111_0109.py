# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0005_auto_20160111_0030'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bar',
            name='creation_date',
        ),
        migrations.RemoveField(
            model_name='bar',
            name='google_id',
        ),
        migrations.RemoveField(
            model_name='bar',
            name='updated_date',
        ),
        migrations.AddField(
            model_name='bar',
            name='gooogle_id',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='bar',
            name='id',
            field=models.TextField(primary_key=True, serialize=False),
        ),
    ]
