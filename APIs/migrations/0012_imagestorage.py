# Generated by Django 3.2.15 on 2023-05-09 12:24

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('APIs', '0011_delete_imagestorage'),
    ]

    operations = [
        migrations.CreateModel(
            name='imageStorage',
            fields=[
                ('imageId', models.AutoField(primary_key=True, serialize=False)),
                ('eventId', models.CharField(max_length=255)),
                ('functionName', models.CharField(max_length=255)),
                ('token', models.CharField(max_length=255)),
                ('image', django.contrib.postgres.fields.ArrayField(base_field=models.ImageField(upload_to=''), size=None)),
                ('createDate', models.DateTimeField(auto_now_add=True)),
                ('modifyDate', models.DateTimeField()),
                ('delFlag', models.BooleanField(default=False)),
            ],
        ),
    ]
