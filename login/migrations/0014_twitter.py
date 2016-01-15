# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0013_remove_bar_twitter'),
    ]

    operations = [
        migrations.CreateModel(
            name='Twitter',
            fields=[
                ('google_id', models.TextField(serialize=False, primary_key=True)),
                ('screen_name', models.TextField(default='')),
                ('created_at', models.DateTimeField(null=True)),
                ('location', models.TextField(default='')),
                ('profile_image', models.TextField(default='')),
                ('profile_banner', models.TextField(default='')),
                ('profile_link_color', models.TextField(default='')),
                ('website', models.TextField(default='')),
            ],
        ),
    ]
