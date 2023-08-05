# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-28 19:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calaccess_raw', '0010_auto_20160726_1425'),
    ]

    operations = [
        migrations.AddField(
            model_name='rawdatafile',
            name='clean_finish_datetime',
            field=models.DateTimeField(help_text='Date and time when the cleaning of the file finished', null=True, verbose_name='date and time cleaning finished'),
        ),
        migrations.AddField(
            model_name='rawdatafile',
            name='clean_start_datetime',
            field=models.DateTimeField(help_text='Date and time when the cleaning of the file started', null=True, verbose_name='date and time cleaning started'),
        ),
        migrations.AddField(
            model_name='rawdatafile',
            name='load_finish_datetime',
            field=models.DateTimeField(help_text='Date and time when the loading of the file finished', null=True, verbose_name='date and time extraction finished'),
        ),
        migrations.AddField(
            model_name='rawdatafile',
            name='load_start_datetime',
            field=models.DateTimeField(help_text='Date and time when the loading of the file started', null=True, verbose_name='date and time loading started'),
        ),
        migrations.AddField(
            model_name='rawdataversion',
            name='download_finish_datetime',
            field=models.DateTimeField(help_text='Date and time when the download of the CAL-ACCESS database export finished', null=True, verbose_name='date and time download finished'),
        ),
        migrations.AddField(
            model_name='rawdataversion',
            name='download_start_datetime',
            field=models.DateTimeField(help_text='Date and time when the download of the CAL-ACCESS database export started', null=True, verbose_name='date and time download started'),
        ),
        migrations.AddField(
            model_name='rawdataversion',
            name='extract_finish_datetime',
            field=models.DateTimeField(help_text='Date and time when extraction of the CAL-ACCESS data files finished', null=True, verbose_name='date and time extraction finished'),
        ),
        migrations.AddField(
            model_name='rawdataversion',
            name='extract_start_datetime',
            field=models.DateTimeField(help_text='Date and time when extraction of the CAL-ACCESS data files started', null=True, verbose_name='date and time extraction started'),
        ),
        migrations.AddField(
            model_name='rawdataversion',
            name='update_finish_datetime',
            field=models.DateTimeField(help_text='Date and time when the update to the CAL-ACCESS version finished', null=True, verbose_name='date and time update finished'),
        ),
        migrations.AddField(
            model_name='rawdataversion',
            name='update_start_datetime',
            field=models.DateTimeField(help_text='Date and time when the update to the CAL-ACCESS version started', null=True, verbose_name='date and time update started'),
        ),
    ]
