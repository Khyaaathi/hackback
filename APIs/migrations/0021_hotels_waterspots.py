# Generated by Django 3.2.15 on 2023-05-15 17:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('APIs', '0020_fooddistribution_foodtypeo'),
    ]

    operations = [
        migrations.CreateModel(
            name='hotels',
            fields=[
                ('hotelId', models.AutoField(primary_key=True, serialize=False)),
                ('eventId', models.CharField(max_length=255)),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('nameO', models.CharField(blank=True, max_length=255, null=True)),
                ('location', models.CharField(max_length=255)),
                ('locationO', models.CharField(max_length=255)),
                ('latitude', models.DecimalField(decimal_places=8, max_digits=10)),
                ('longitude', models.DecimalField(decimal_places=8, max_digits=10)),
                ('openingTime', models.TimeField()),
                ('openingTimeO', models.TimeField()),
                ('closingTime', models.TimeField()),
                ('closingTimeO', models.TimeField()),
                ('message', models.CharField(blank=True, max_length=255, null=True)),
                ('messageO', models.CharField(blank=True, max_length=255, null=True)),
                ('contactNumber', models.IntegerField(blank=True, null=True)),
                ('alternateNumber', models.IntegerField(blank=True, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('starRating', models.IntegerField(blank=True, null=True)),
                ('createDate', models.DateTimeField(auto_now_add=True)),
                ('modifyDate', models.DateTimeField()),
                ('delFlag', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='waterSpots',
            fields=[
                ('waterSpotsId', models.AutoField(primary_key=True, serialize=False)),
                ('eventId', models.CharField(max_length=255)),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('nameO', models.CharField(blank=True, max_length=255, null=True)),
                ('location', models.CharField(max_length=255)),
                ('locationO', models.CharField(max_length=255)),
                ('latitude', models.DecimalField(decimal_places=8, max_digits=10)),
                ('longitude', models.DecimalField(decimal_places=8, max_digits=10)),
                ('openingTime', models.TimeField()),
                ('openingTimeO', models.TimeField()),
                ('closingTime', models.TimeField()),
                ('closingTimeO', models.TimeField()),
                ('message', models.CharField(blank=True, max_length=255, null=True)),
                ('messageO', models.CharField(blank=True, max_length=255, null=True)),
                ('working', models.BooleanField()),
                ('createDate', models.DateTimeField(auto_now_add=True)),
                ('modifyDate', models.DateTimeField()),
                ('delFlag', models.BooleanField(default=False)),
            ],
        ),
    ]
