# Generated by Django 4.0.4 on 2022-05-07 06:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vulscan', '0002_solupload_fname'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='solupload',
            name='sol',
        ),
        migrations.AddField(
            model_name='solupload',
            name='add',
            field=models.CharField(max_length=100, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='solupload',
            name='scantype',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='solupload',
            name='result',
            field=models.CharField(max_length=1000, null=True),
        ),
    ]
