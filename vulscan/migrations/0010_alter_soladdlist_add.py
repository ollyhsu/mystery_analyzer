# Generated by Django 4.0.4 on 2022-05-07 12:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vulscan', '0009_alter_soladdlist_result'),
    ]

    operations = [
        migrations.AlterField(
            model_name='soladdlist',
            name='add',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
