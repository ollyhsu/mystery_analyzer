# Generated by Django 4.0.4 on 2022-05-07 11:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vulscan', '0006_soladdlist_uid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='soladdlist',
            name='result',
            field=models.CharField(max_length=10000, null=True),
        ),
    ]
