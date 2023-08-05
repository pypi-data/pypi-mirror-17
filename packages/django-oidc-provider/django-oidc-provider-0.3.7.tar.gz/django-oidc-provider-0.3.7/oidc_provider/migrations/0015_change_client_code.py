# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-10 13:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oidc_provider', '0014_client_jwt_alg'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='_redirect_uris',
            field=models.TextField(default='', help_text='Enter each URI on a new line.', verbose_name='Redirect URI'),
        ),
        migrations.AlterField(
            model_name='client',
            name='client_secret',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='client',
            name='client_type',
            field=models.CharField(choices=[('confidential', 'Confidential'), ('public', 'Public')], default='confidential', help_text='<b>Confidential</b> clients are capable of maintaining the confidentiality of their credentials. <b>Public</b> clients are incapable.', max_length=30),
        ),
        migrations.AlterField(
            model_name='client',
            name='jwt_alg',
            field=models.CharField(choices=[('HS256', 'HS256'), ('RS256', 'RS256')], default='RS256', max_length=10, verbose_name='JWT Algorithm'),
        ),
        migrations.AlterField(
            model_name='client',
            name='name',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='client',
            name='response_type',
            field=models.CharField(choices=[('code', 'code (Authorization Code Flow)'), ('id_token', 'id_token (Implicit Flow)'), ('id_token token', 'id_token token (Implicit Flow)')], max_length=30),
        ),
        migrations.AlterField(
            model_name='code',
            name='_scope',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='code',
            name='nonce',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='token',
            name='_scope',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='userconsent',
            name='_scope',
            field=models.TextField(default=''),
        ),
    ]
