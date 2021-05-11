from django.db import connection
def dictGetColumn(cursor):
    "Return all columns of select statement"
    columns = [col[0] for col in cursor.description]
    return columns

def get_sql_type(query):
    splited_query=query.split(" ")
    return splited_query[0].lower()

def is_dsl(query):
    
    return get_sql_type(query) == "select"

def is_user_epidemiologist(user):
    return is_user_id_epidemiologist(user.id)

def is_user_id_epidemiologist(user_id):
    with connection.cursor() as cursor:
            cursor.execute("""SELECT e.uuid 
                            FROM utilisateur u join epidemiologiste e ON u.uuid=e.uuid
                            WHERE u.id=%s""", [user_id])
            
            row = cursor.fetchone()
    return row is not None