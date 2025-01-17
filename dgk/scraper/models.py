from django.db import models

class Skelbimas(models.Model):
    pavadinimas = models.CharField(max_length=255, unique=True) # pavadinimas
    vykdytojoPavadinimas = models.CharField(max_length=255) # vykdytojo Pavadinimas
    nuoroda = models.URLField() # nuoroda
    data = models.DateField() # data
    terminas = models.DateField() # terminas
    bvpzKodas = models.CharField(max_length=50) # bvpz kodas
    skelbimoTipas = models.CharField(max_length=100) # pirkimo tipas

    def __str__(self):
        return self.pavadinimas
    
class User(models.Model):
    username = models.CharField(max_length=50)
    email = models.EmailField(unique = True)
    password = models.CharField(max_length=50)

    def __str__(self):
        return self.username