# Generated by Django 3.2.15 on 2023-05-24 05:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('APIs', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='parking_user',
            fields=[
                ('parkingXuser', models.AutoField(primary_key=True, serialize=False)),
                ('eventId', models.CharField(max_length=255)),
                ('parkingId', models.CharField(max_length=255)),
                ('userId', models.CharField(max_length=255)),
                ('createDate', models.DateTimeField(auto_now_add=True)),
                ('modifyDate', models.DateTimeField(auto_now=True)),
                ('delFlag', models.BooleanField(default=False)),
            ],
        ),
    ]
