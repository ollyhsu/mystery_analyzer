# Generated by Django 4.0.4 on 2022-05-12 07:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vulscan', '0017_soladdlist_check_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='soladdlist',
            name='cfg',
            field=models.TextField(blank=True, null=True),
        ),
    ]
