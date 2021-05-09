from django import forms
from django.db import connection
from django.core.exceptions import ValidationError
def username_already_used(username):
    print("Le nom que je veux est / " +username)
    with connection.cursor() as cursor:
        cursor.execute("""SELECT id
                            FROM utilisateur 
                            WHERE pseudo=%s""", [username])
            
        return cursor.fetchone() is not None
def validate_password(pwd):
    conds = {
        "uppercase": lambda s: any(x.isupper() for x in s),
        "lowercase": lambda s: any(x.islower() for x in s),
        "number": lambda s: any(x.isdigit() for x in s),
        "length": lambda s: len(s) >= 8
    }

    valid = True
    for name, cond in conds.items():
        if not cond(pwd):
            return name
    return None
def simple_validate_password(pwd):
    conds = [
        lambda s: any(x.isupper() for x in s),
        lambda s: any(x.islower() for x in s),
        lambda s: any(x.isdigit() for x in s),
        lambda s: len(s) >= 8
    ]

    return all(cond(pwd) for cond in conds)
def get_string_pswd_error(pwd):

    error_type = validate_password(pwd)
    if(error_type=="uppercase"):
        return "Le mot de passe doit contenir au moins une majuscule"
    elif(error_type=="lowercase"):
         return "Le mot de passe doit contenir au moins une minuscule"
    elif(error_type=="number"):
         return "Le mot de passe doit contenir au moins un nombre"
    elif(error_type=="length"):
         return "Le mot de passe doit être de taille 8 minimum"
    else :
        return None
    

class QueryForm(forms.Form):
    query = forms.CharField(label='Your name', max_length=100, required=True)

class CreateUserForm(forms.Form):
    uuid = forms.CharField(label="uuid", max_length=150, required=False, help_text="Si vide, un uuid aléatoire sera généré")
    nom = forms.CharField(label="Nom", max_length=40, required=True)
    prenom = forms.CharField(label="Prénom", max_length=40, required=True)
    pseudo = forms.CharField(label="Pseudo", max_length=40, required=True)
    mot_de_passe = forms.CharField(label="Mot de passe",widget=forms.PasswordInput(),
     max_length=100, required=True,
      help_text="""Le mot de passe doit contenir une majuscule, une minuscule,
       un nombre et doit être de minimum 8 caractères""")
    rue_adresse = forms.CharField(label="Nom de rue", max_length=100, required=False)
    numero_adresse = forms.IntegerField(label="Numéro rue", required=False)
    code_postal_adresse = forms.IntegerField(label="Code postal", required=False)
    ville_adresse = forms.CharField(label="Ville", max_length=40, required=False)

    
    def clean_mot_de_passe(self):
        data = self.cleaned_data['mot_de_passe']
        error = get_string_pswd_error(data)
        if error:
            raise ValidationError(error)
        return data
    def clean_pseudo(self):
        data = self.cleaned_data['pseudo']
       
        if username_already_used(data):
            raise ValidationError("HOLY SHIEEEET!!! Le nom d'utilisateur est déjà pris!")
        return data
    
    def clean(self):
        cleaned_data = super().clean()
        array = []
        rue_adresse = cleaned_data.get("rue_adresse")
        numero_adresse = cleaned_data.get("numero_adresse")
        code_postal_adresse = cleaned_data.get("code_postal_adresse")
        ville_adresse = cleaned_data.get("ville_adresse")
        if rue_adresse:
            array.append(rue_adresse)
        if numero_adresse:
            array.append(numero_adresse)
        if code_postal_adresse:
            array.append(code_postal_adresse)
        if ville_adresse:
            array.append(ville_adresse)

        if len(array) > 0 and len(array) <4:
            
            raise ValidationError("Si un champs adresse est rempli, ils doivent tous l'être")
class CreateEpidemiologistForm(CreateUserForm):
    centre = forms.CharField(label="Centre", max_length=40, required=True)
    telephone_service = forms.CharField(label="Telephone service", max_length=40, required=True)

