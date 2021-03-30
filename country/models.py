from django.db import models

# Create your models here.
class Country(models.Model):

    iso = models.CharField("ISO", max_length=3, primary_key=True)
    name = models.CharField("nom", max_length=50, unique=True)
    hdi = models.FloatField("HDI")
    population = models.BigIntegerField()
    surface = models.BigIntegerField()
    start_vaccination_date = models.DateField( auto_now=False, auto_now_add=False)

    

    def __str__(self):
        return self.name

    #def get_absolute_url(self):
    #    return reverse("_detail", kwargs={"pk": self.pk})
class Climat(models.Model):
    description = models.TextField()

    def __str__(self):
        return self.description
