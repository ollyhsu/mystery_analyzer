# Generated by Django 4.0.4 on 2022-05-07 07:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vulscan', '0005_soladdlist_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='soladdlist',
            name='uid',
            field=models.IntegerField(null=True),
        ),
    ]
