# Generated by Django 3.2.15 on 2023-05-15 06:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('APIs', '0018_fooddistribution_prefereddate'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fooddistribution',
            name='cuisine',
        ),
        migrations.RemoveField(
            model_name='fooddistribution',
            name='cuisineO',
        ),
        migrations.AddField(
            model_name='fooddistribution',
            name='foodType',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='fooddistribution',
            name='numberOfBeneficiary',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
