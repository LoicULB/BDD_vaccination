from django.contrib.auth.backends import BaseBackend
from django.db import connection
from django.contrib.auth.models import User
import uuid
from django.contrib.auth.hashers import make_password, check_password

def is_valid_uuid(val):
    try:
        uuid.UUID(str(val))
        return True
    except ValueError:
        return False
class MyBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        if(is_valid_uuid(username)):
            with connection.cursor() as cursor:
                cursor.execute("SELECT mot_de_passe FROM Utilisateur WHERE uuid=%s", [username])
            
                row = cursor.fetchone()
                if (check_password(password, row[0])):
                   
                    return User(id=username)
        else :
            with connection.cursor() as cursor1:
                cursor1.execute("SELECT id, mot_de_passe FROM Utilisateur WHERE pseudo=%s", [username])
            
                row2 = cursor1.fetchone()
                if (check_password(password, row2[1])):
                    try:
                        user = User.objects.get(id=row2[0])
                    except User.DoesNotExist:
                        # Create a new user. There's no need to set a password
                        # because only the password from settings.py is checked.
                        user = User(id=row2[0], username=username)
                
                        user.save()
                    return user
        
        
    def get_user(self, user_id):
        return User.objects.get(id=user_id)
       