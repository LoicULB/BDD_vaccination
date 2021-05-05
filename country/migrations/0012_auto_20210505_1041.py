
# Generated by Django 3.1.7 on 2021-03-23 20:05
import os
from pathlib import Path
from django.db import migrations, models

from django.conf import settings
from django.conf.urls.static import static
def get_sql_from_file(filepath):
        #read whole file to a string
        text_file = open(filepath, "r")
        data = text_file.read()
 
        #close file
        text_file.close()
        
        return data 
class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('country', '0011_insert_stats_hopsitalisation'),
    ]
    
    operations = [
        migrations.RunSQL(
            sql=[(get_sql_from_file(os.path.join(settings.STATICFILES_DIRS[0], 'ressources/sql_file_reader/insert_usable_user.sql')))],
            reverse_sql=[(get_sql_from_file(os.path.join(settings.STATICFILES_DIRS[0], 'ressources/sql_file_reader/reverse_insert_usable_user.sql')))]
        )
    ]