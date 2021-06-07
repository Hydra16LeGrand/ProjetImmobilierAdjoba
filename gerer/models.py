from django.db import models

# Create your models here.

class Utilisateur(models.Model):

	nom = models.CharField(max_length=30)
	prenom = models.CharField(max_length=50)
	contact = models.CharField(max_length=20)
	email = models.EmailField()
	cin = models.CharField(max_length=30, blank=True)
	adresse = models.CharField(max_length=100)

class Bien(models.Model):

	localisation = models.TextField()
	dimensions = models.IntegerField()
	prix = models.FloatField()
	image = models.ImageField(upload_to = 'bien', blank = True)

	def get_image(self):

		if self.image and hasattr(self.image, 'url'):
			return self.image.url

		else:
			return '/media/bien/pas_d_image.jpg'

class Terrain(Bien):

	description = models.TextField(blank=True)
	status = models.CharField(max_length=10)
	email = models.EmailField(blank=True)
	
	# utilisateur = models.ForeignKey(Utilisateur, on_delete = models.CASCADE, blank = True)

class Maison(Bien):

	type_maison = models.CharField(max_length=100)
	nbre_chambre = models.IntegerField()
	nbre_sallon = models.IntegerField()
	nbre_douche = models.IntegerField()
	nbre_garage = models.IntegerField()
	nbre_cuisine = models.IntegerField()
	autre_detail = models.TextField(blank=True)
	status = models.CharField(max_length=10)
	email = models.EmailField(blank=True)

	
	# utilisateur = models.ForeignKey(Utilisateur, on_delete = models.CASCADE, blank = True)	

class Agent(models.Model):

	nom = models.CharField(max_length=100)
	role = models.CharField(max_length=50)
	nbre_vente = models.IntegerField()
	profil = models.ImageField(upload_to='agent', blank=True)

	def get_profil(self):

		if self.profil and hasattr(self.profil, 'url'):
			return self.profil.url

		else:
			return '/media/bien/pas_de_profil.jpg'