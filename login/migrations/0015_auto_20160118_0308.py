# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0014_twitter'),
    ]

    operations = [
        migrations.AddField(
            model_name='twitter',
            name='statuses',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='twitter',
            name='tweet_attributes',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='twitter',
            name='updated_date',
            field=models.DateTimeField(null=True),
        ),
    ]
