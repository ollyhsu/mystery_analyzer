# Generated by Django 4.0.4 on 2022-05-07 02:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vulscan', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='solupload',
            name='fname',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
