# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-26 14:49
from __future__ import unicode_literals

import calaccess_raw.annotations
import calaccess_raw.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('calaccess_raw', '0004_auto_20160804_1758'),
    ]

    operations = [
        migrations.AlterField(
            model_name='receivedfilingscd',
            name='filing_directory',
            field=calaccess_raw.fields.CharField(db_column='FILING_DIRECTORY', help_text='This field is undocumented', max_length=60),
        ),
        migrations.AlterField(
            model_name='receivedfilingscd',
            name='filing_file_name',
            field=calaccess_raw.fields.CharField(db_column='FILING_FILE_NAME', help_text='The field is undocumented', max_length=60),
        ),
        migrations.AlterField(
            model_name='receivedfilingscd',
            name='form_id',
            field=calaccess_raw.fields.CharField(blank=True, choices=[(b'F400', b'Form 400: Statement of Organization (Slate Mailer Organization)'), (b'F401', b'Form 401: Slate Mailer Organization Campaign Statement'), (b'F402', b'Form 402: Statement of Termination (Slate Mailer Organization)'), (b'F410', b'Form 410: Statement of Organization Recipient Committee'), (b'F425', b'Form 425: Semi-Annual Statement of no Activity'), (b'F450', b'Form 450: Recipient Committee Campaign Disclosure Statement - Short Form'), (b'F460', b'Form 460: Recipient Committee Campaign Statement'), (b'F461', b'Form 461: Independent Expenditure Committee & Major Donor Committee Campaign Statement'), (b'F465', b'Form 465: Supplemental Independent Expenditure Report'), (b'F496', b'Form 496: Late Independent Expenditure Report'), (b'F497', b'Form 497: Late Contribution Report'), (b'F498', b'Form 498: Slate Mailer Late Payment Report'), (b'F601', b'Form 601: Lobbying Firm Registration Statement'), (b'F602', b'Form 602: Lobbying Firm Activity Authorization'), (b'F603', b'Form 603: Lobbyist Employer or Lobbying Coalition Registration Statement'), (b'F604', b'Form 604: Lobbyist Certification Statement'), (b'F606', b'Form 606: Notice of Termination'), (b'F607', b'Form 607: Notice of Withdrawal'), (b'F615', b'Form 615: Lobbyist Report'), (b'F625', b'Form 625: Report of Lobbying Firm'), (b'F635', b'Form 635: Report of Lobbyist Employer or Report of Lobbying Coalition'), (b'F645', b'Form 645: Report of Person Spending $5,000 or More')], db_column='FORM_ID', documentcloud_pages=[calaccess_raw.annotations.DocumentCloud(end_page=8, id='2711624-Overview', start_page=4)], help_text='Form identification code', max_length=7, verbose_name='form identification code'),
        ),
        migrations.AlterField(
            model_name='receivedfilingscd',
            name='receive_comment',
            field=calaccess_raw.fields.CharField(db_column='RECEIVE_COMMENT', help_text='A comment', max_length=120),
        ),
    ]
