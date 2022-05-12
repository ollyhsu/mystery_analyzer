# Generated by Django 4.0.4 on 2022-05-12 13:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mytools', '0003_etherverified_fpath'),
    ]

    operations = [
        migrations.CreateModel(
            name='EtherDeatilList',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('rid', models.IntegerField(null=True)),
                ('swcid', models.IntegerField(null=True)),
                ('title', models.CharField(max_length=100, null=True)),
                ('impact', models.CharField(max_length=100, null=True)),
                ('description', models.CharField(max_length=100, null=True)),
                ('lines', models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='etherverified',
            name='cfg',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='etherverified',
            name='check_time',
            field=models.CharField(max_length=100, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='etherverified',
            name='result',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='etherverified',
            name='runtime',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='etherverified',
            name='status',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
