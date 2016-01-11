# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0008_auto_20160111_0151'),
    ]

    operations = [
        migrations.CreateModel(
            name='Twitter',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
            ],
        ),
        migrations.AddField(
            model_name='bar',
            name='creation_date',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='bar',
            name='updated_date',
            field=models.DateTimeField(null=True),
        ),
    ]
