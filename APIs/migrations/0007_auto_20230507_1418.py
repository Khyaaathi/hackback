# Generated by Django 3.2.15 on 2023-05-07 08:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('APIs', '0006_auto_20230507_1416'),
    ]

    operations = [
        migrations.AlterField(
            model_name='founditem',
            name='description',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='grievance',
            name='description',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='lostitem',
            name='description',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]
