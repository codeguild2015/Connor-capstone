# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0003_auto_20160111_0012'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bar',
            name='creation_date',
            field=models.DateTimeField(default=''),
        ),
        migrations.AlterField(
            model_name='bar',
            name='google_id',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='bar',
            name='id',
            field=models.TextField(serialize=False, default='', primary_key=True),
        ),
        migrations.AlterField(
            model_name='bar',
            name='latitude',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='bar',
            name='longitude',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='bar',
            name='name',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='bar',
            name='open_at_update',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='bar',
            name='price_level',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='bar',
            name='rating',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='bar',
            name='updated_date',
            field=models.DateTimeField(default=''),
        ),
        migrations.AlterField(
            model_name='bar',
            name='vicinity',
            field=models.TextField(default=''),
        ),
    ]
