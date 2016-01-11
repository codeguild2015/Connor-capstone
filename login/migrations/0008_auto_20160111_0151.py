# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0007_auto_20160111_0109'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bar',
            name='id',
            field=models.AutoField(serialize=False, primary_key=True),
        ),
        migrations.AlterField(
            model_name='bar',
            name='latitude',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='bar',
            name='longitude',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='bar',
            name='price_level',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='bar',
            name='rating',
            field=models.TextField(default=''),
        ),
    ]
