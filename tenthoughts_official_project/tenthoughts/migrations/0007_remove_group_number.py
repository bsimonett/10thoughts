# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tenthoughts', '0006_group_number'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='group',
            name='number',
        ),
    ]
