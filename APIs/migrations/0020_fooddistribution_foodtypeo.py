# Generated by Django 3.2.15 on 2023-05-15 07:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('APIs', '0019_auto_20230515_1215'),
    ]

    operations = [
        migrations.AddField(
            model_name='fooddistribution',
            name='foodTypeO',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
