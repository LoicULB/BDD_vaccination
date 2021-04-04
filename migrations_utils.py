import os
from pathlib import Path
from django.conf import settings
from django.conf.urls.static import static
def get_sql_from_file(filepath):
        #read whole file to a string
        text_file = open(filepath, "r")
        data = text_file.read()
 
        #close file
        text_file.close()
        
        return data 

def get_sql_from_ressources_files(filepath):
     return   get_sql_from_file(os.path.join(settings.STATICFILES_DIRS[0], f"ressources/{filepath}"))