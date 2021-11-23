from django.db import migrations
from yamod import models

def create_genres(apps,schema_editor):
    for name in ["Action","Horror","Scifi","Drama","Comedy"]: 
        models.Genre.objects.get_or_create(name=name)

class Migration(migrations.Migration):

    dependencies = [
        ('yamod', '0009_alter_season_unique_together'),
    ]

    operations = [
        migrations.RunPython(create_genres),
    ]
