# Generated by Django 3.2.8 on 2021-11-04 05:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('yamod', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='original_title',
            field=models.CharField(max_length=1024, null=True),
        ),
        migrations.AlterField(
            model_name='roletype',
            name='name',
            field=models.CharField(max_length=1024, unique=True),
        ),
    ]
