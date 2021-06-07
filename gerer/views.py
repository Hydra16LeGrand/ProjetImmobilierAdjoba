from django.shortcuts import render, redirect
import pyrebase
from django.contrib.auth import logout
from . import models
# Create your views here.


firebaseConfig = {
    "apiKey": "AIzaSyA5q9GAYhxFfer_SSgrvfEiAJgKn9OsueI",
    "authDomain": "projet-immobilier-8277f.firebaseapp.com",
    "databaseURL": "https://projet-immobilier-8277f-default-rtdb.firebaseio.com",
    "projectId": "projet-immobilier-8277f",
    "storageBucket": "projet-immobilier-8277f.appspot.com",
    "messagingSenderId": "1088189141977",
    "appId": "1:1088189141977:web:31e57026f78aba97817fc8",
    "measurementId": "G-TJWV1D1KQQ"

}
firebase = pyrebase.initialize_app(firebaseConfig)
authentification = firebase.auth()
database = firebase.database()

class Acces:

	def inscription(request):

		if request.method == 'POST':

			form = request.POST

			if form.get('mdp') == form.get('c_mdp') and len(form.get('mdp')) >= 6:

				try:
					utilisateur = authentification.create_user_with_email_and_password(form.get('email'), form.get('mdp'))
				except:
					return render(request, 'inscription.html', {'message': "Erreur lors de la creation du compte"})
				else:
					try:
						models.Utilisateur.objects.create(

							nom = form.get('nom'),
							prenom = form.get('prenom'),
							contact = form.get('contact'),
							email = form.get('email'),
							cin = form.get('cin'),
							adresse = form.get('adresse')
							)
						authentification.send_email_verification(utilisateur['idToken'])
					except Exception as e:
						raise e
						# return render(request, 'inscription.html', {'message': "Erreur lors de la creation du compte"})
					else:
						return render(request, 'authentification.html', {'message': "Veuillez cliquer sur le lien recu par e-mail pour la confirmation de votre compte"})

			else:
				return render(request, "inscription.html", {'message':"Les mots de passe ne correspondent pas ou sont inferieurs a 6 caracteres"})

		else:
			return render(request, "inscription.html")


	def authentification(request):

		if request.method == 'POST':
			form = request.POST

			try:
				utilisateur = authentification.sign_in_with_email_and_password(form.get('email'), form.get('mdp'))
			except Exception as e:
				# raise e
				return render(request, 'authentification.html', {'message': "Session expire. Verifiez votre connexion et reessayer"})
			else:
				try:
					infos = authentification.get_account_info(utilisateur['idToken'])
				except Exception as e:
					# raise e
					return render(request, "authentification.html", {'message': "Impossible de reccuperer les informations sur cet utilisateur"})
				else:
					emailVerified = infos['users'][0]['emailVerified']

					if emailVerified:
						request.session['uid'] = str(utilisateur['idToken'])

						return redirect('index')

					else:
						return render(request, 'authentification.html', {'message': "Veuillez activez d'abord votre compte avec le lien recu par mail"})

		else:
			return render(request, "authentification.html")

	def dashboard(request):

		try:
			mon_idToken = request.session['uid']
		except :
			return redirect('authentification')
		else:
			try:
				infos = authentification.get_account_info(mon_idToken)
				uid = infos['users'][0]['localId']
			except :
				return render(request, 'authentification.html', {'message': "Les informations concernant cet utilisateur n'existe plus"})
			else:
				return render(request, "dashboard.html", {'email':infos['users'][0]['email']})

	def deconnexion(request):

		# Deconnexion de l'utilisateur
		logout(request)
		return redirect('authentification')

class Maison:

	def lister(request):

		return render(request, "maison/lister.html", {"maisons":models.Maison.objects.all(), 'agents': models.Agent.objects.all(), "deco": "deco"})

	def acheter(request, id_maison):

		try:
			mon_idToken = request.session['uid']
		except :
			return redirect('authentification')
		else:
			try:
				infos = authentification.get_account_info(mon_idToken)
				uid = infos['users'][0]['localId']
			except :
				return render(request, 'authentification.html', {'message': "Les informations concernant cet utilisateur n'existe plus", "deco": "deco"})
			else:
				try:
					mon_idToken = request.session['uid']
					# print(mon_idToken)	
				except :
					return redirect('authentification')
				else:
					
					try:
						infos = authentification.get_account_info(mon_idToken)
						# uid = infos['users'][0]['localId']
						email = infos['users'][0]['email']
					except Exception as e:
						return render(request, "maison/lister.html", {'message': "Desole ajout refuse. Veuillez nous contactez pour plus d'informations"})
					else:
						try:
							utilisateur = models.Utilisateur.objects.get(email = email)
							print(email)
							maison = models.Maison.objects.get(id = id_maison)
							maison.email = email
							maison.save()
						except Exception as e:
							return render(request, "maison/lister.html", {'message': "Erreur lors de l'ajout de la maison"})
						else:
							maisons = []
							for maison in models.Maison.objects.all():
								print(maison.email)
								print(email)
								if maison.email == email and maison.status == "a_acheter":
									maisons.append(maison)
							return render(request, "maison/acheter.html", {
								'message':"Maison ajoute a la liste des envies. Nous vous contacterons dans les plus brefs delai", 
								'maisons': maisons, 
								"utilisateur":utilisateur})

	def a_acheter(request):

		try:
			mon_idToken = request.session['uid']
		except :
			return redirect('authentification')
		else:
			try:
				infos = authentification.get_account_info(mon_idToken)
				uid = infos['users'][0]['localId']
			except :
				return render(request, 'authentification.html', {'message': "Les informations concernant cet utilisateur n'existe plus"})
			else:
				maisons = []
				for maison in models.Maison.objects.all():
					print (maison.utilisateur)
					if maison.email == email and maison.status == "a_acheter":
						maisons.append(maison)

				return render(request, "maison/acheter.html", {'maisons': maisons, "deco": "deco"})

	def confirmer_achat(request):

		try:
			mon_idToken = request.session['uid']
		except :
			return redirect('authentification')
		else:
			try:
				infos = authentification.get_account_info(mon_idToken)
				uid = infos['users'][0]['localId']
			except :
				return render(request, 'authentification.html', {'message': "Les informations concernant cet utilisateur n'existe plus"})
			else:
				return render(request, "maison/lister.html", {
					"maisons": models.Maison.objects.all(),
					"message": "Choix confirmer. Nous vous contacterons dans les plus brefs delai",
					"agents":models.Agent.objects.all(),
					"deco":""
					})

	def louer_lister(request):

		return render(request, "maison/a_louer/lister.html", {"maisons":models.Maison.objects.filter(status="a_louer")})

	def louer(request, id_maison):
		try:
			mon_idToken = request.session['uid']
			# print(mon_idToken)
		except :
			return redirect('authentification')
		else:
			
			try:
				
				infos = authentification.get_account_info(mon_idToken)
				# uid = infos['users'][0]['localId']
				email = infos['users'][0]['email']
				# print(email)
			except Exception as e:
				# return render(request, "maison/a_louer/lister.html", {'message': "Erreur lors de la reccuperation des infos utilisateur"})
				raise e
			else:
				try:
					utilisateur = models.Utilisateur.objects.get(email = email)
					maison = models.Maison.objects.get(id = id_maison)
					maison.email = email
					maison.save()
				except Exception as e:
					return render(request, "maison/a_louer/lister.html", {'message': "Erreur lors de l'ajout de la maison"})
				else:
					
					maisons = []
					for maison in models.Maison.objects.all():
						print (maison.email)
						if maison.email == email and maison.status == "a_louer":
							maisons.append(maison)
					return render(request, "maison/a_louer/louer.html", {
						'message':"Maison ajoute a la liste des envies. Nous vous contacterons dans les plus brefs delai", 
						'maisons': maisons})

	def a_louer(request):

		maisons = []
		for maison in models.Maison.objects.all():
			
			if maison.email == email and maison.status == "a_louer":
				maisons.append(maison)

		return render(request, "maison/a_louer/louer.html", {'maisons': maisons})

	def vendre(request):
		return render(request)

class Terrain:

	def lister(request):

		try:
			mon_idToken = request.session['uid']
		except :
			return redirect('authentification')
		else:
			try:
				infos = authentification.get_account_info(mon_idToken)
				uid = infos['users'][0]['localId']
			except :
				return render(request, 'authentification.html', {'message': "Les informations concernant cet utilisateur n'existe plus"})
			else:
				print("yo")
				return render(request, "terrain/lister.html", {"terrains":models.Terrain.objects.all(), "agents": models.Agent.objects.all(), "deco": "deco"})


	def acheter(request, id_terrain):

		try:
			mon_idToken = request.session['uid']
		except :
			return redirect('authentification')
		else:
			try:
				infos = authentification.get_account_info(mon_idToken)
				uid = infos['users'][0]['localId']
			except:
				return render(request, 'authentification.html', {'message': "Les informations concernant cet utilisateur n'existe plus"})
			else:
				try:
					mon_idToken = request.session['uid']
				except :
					return redirect('authentification')
				else:
					
					try:
						infos = authentification.get_account_info(mon_idToken)
						email = infos['users'][0]['email']
					except Exception as e:
						return render(request, "terrain/lister.html", {'message': "Erreur lors de l'ajout du terrain"})
					else:
						try:
							utilisateur = models.Utilisateur.objects.get(email = email)
							terrain = models.Terrain.objects.get(id = id_terrain)
							terrain.email = email
							terrain.save()
						except Exception as e:
							return render(request, "terrain/lister.html", {'message': "Erreur lors de l'ajout du terrain"})

						else:
							terrains = []

							for terrain in models.Terrain.objects.all():
								if terrain.email == email and terrain.status == "a_acheter":
									terrains.append(terrain)

							return render(request, "terrain/acheter.html", {
								'message':"Terrain ajoute a la liste des envies. Nous vous contacterons dans les plus brefs delai",
								'terrains': terrains, "deco": "deco"})

	def a_acheter(request):

		terrains = []

		try:
			mon_idToken = request.session['uid']
		except :
			return redirect('authentification')
		else:
			try:
				infos = authentification.get_account_info(mon_idToken)
				uid = infos['users'][0]['localId']
			except :
				return render(request, 'authentification.html', {'message': "Les informations concernant cet utilisateur n'existe plus"})
			else:
				for terrain in models.Terrain.objects.all():
					
					if terrain.utilisateur:
						terrains.append(terrain)

				return render(request, "terrain/acheter.html", {'terrains': terrains, "deco": "deco"})

	def confirmer_achat(request):

		try:
			mon_idToken = request.session['uid']
		except :
			return redirect('authentification')
		else:
			try:
				infos = authentification.get_account_info(mon_idToken)
				uid = infos['users'][0]['localId']
			except :
				return render(request, 'authentification.html', {'message': "Les informations concernant cet utilisateur n'existe plus"})
			else:
				return render(request, "terrain/lister.html", {"message": "Choix confirmer. Nous vous contacterons dans les plus brefs delai", "deco": "deco"})

	def louer(request):
		return render(request)

	def vendre(request):
		return render(request)
		
def index(request):

	try:
		mon_idToken = request.session['uid']
	except :
		return render(request, "index.html", {"agents":models.Agent.objects.all()})
	else:
		try:
			infos = authentification.get_account_info(mon_idToken)
			uid = infos['users'][0]['localId']
		except :
			return render(request, "index.html", {"agents":models.Agent.objects.all()})
		else:
			return render(request, "index.html", {"agents":models.Agent.objects.all(), "deco":"deco"})
	
def a_propos(request):

	try:
		mon_idToken = request.session['uid']
	except :
		return redirect('authentification')
	else:
		try:
			infos = authentification.get_account_info(mon_idToken)
			uid = infos['users'][0]['localId']
		except :
			return render(request, 'authentification.html', {'message': "Les informations concernant cet utilisateur n'existe plus"})
		else:
			return render(request, "a_propos.html", {"agents":models.Agent.objects.all(), "deco":"deco"})

def contact(request):

	try:
		mon_idToken = request.session['uid']
	except :
		return redirect('authentification')
	else:
		try:
			infos = authentification.get_account_info(mon_idToken)
			uid = infos['users'][0]['localId']
		except :
			return render(request, 'authentification.html', {'message': "Les informations concernant cet utilisateur n'existe plus"})
		else:
			return render(request, "contact.html", {"deco":"deco"})