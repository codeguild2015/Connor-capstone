# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0002_item_text'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bar',
            fields=[
                ('id', models.TextField(primary_key=True, serialize=False)),
                ('name', models.TextField()),
                ('latitude', models.IntegerField()),
                ('longitude', models.IntegerField()),
                ('google_id', models.TextField()),
                ('vicinity', models.TextField()),
                ('price_level', models.IntegerField()),
                ('rating', models.IntegerField()),
                ('creation_date', models.DateTimeField()),
                ('updated_date', models.DateTimeField()),
                ('open_at_update', models.TextField()),
            ],
        ),
        migrations.DeleteModel(
            name='Item',
        ),
    ]
