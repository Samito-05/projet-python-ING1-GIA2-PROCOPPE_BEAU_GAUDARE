from python.models import Film, Salle, Utilisateur
from python.visuals import ascii_art, clear_screen
from python.admin import admin_menu
from python.user import user_menu
import storage
import getpass
import time


def print_header():
    clear_screen()
    print(ascii_art("CY-NEMA  APP"))

def menu():
	while True:
		print_header()
		print('\n')
		print('1) Afficher les films')
		print('2) Se connecter')
		print('3) Créer un compte utilisateur')
		print('4) Acceder au panneau d\'administration')
		print('0) Quitter')
		print('\n')
		choix = input('Choix: ').strip()
		if choix == '1':
			films = storage.list_films()
			if not films:
				print('\n')
				print('Aucun film.')
			for f in films:
				print(f"- {f.titre}: {f.duree}min [{f.categorie}] (Age minimum={f.age_min}) {f.horaires}")
			print('\n')
			input('Appuyez sur Entrée pour revenir au menu...')
		elif choix == '2':
			email = input('Email: ')
			pwd = getpass.getpass('Mot de passe: ')
			u = storage.authenticate_user(email, pwd)
			if u:
				print(f'Authentification réussie. Bonjour {u.prenom} {u.nom} (role={u.role})')
				input('Appuyez sur Entrée pour continuer...')
				user_menu(u)
			else:
				print('Email ou mot de passe invalide.')
				input('Appuyez sur Entrée pour revenir au menu...')
		elif choix == '3':
			nom = input('Nom: ')
			prenom = input('Prénom: ')
			dob = input('Date de naissance (YYYY-MM-DD): ')
			email = input('Email: ')
			pwd = getpass.getpass('Mot de passe: ')
			try:
				u = storage.create_user(nom=nom, prenom=prenom, date_naissance=dob, email=email, password=pwd)
				print(f'Compte créé pour {u.email} (id={u.id})')
				input('Appuyez sur Entrée pour revenir au menu...')
				user_menu(u)
			except ValueError as e:
				print('Erreur:', e)
		elif choix == '4':
			email = input('Email: ')
			pwd = getpass.getpass('Mot de passe: ')
			u = storage.authenticate_admin(email, pwd)
			if u:
				print(f'Authentification réussie. Bonjour {u.prenom} {u.nom} (role={u.role})')
				input('Appuyez sur Entrée pour continuer...')
				admin_menu(u)
			else:
				print('Email ou mot de passe invalide.')
				input('Appuyez sur Entrée pour revenir au menu...')
		elif choix == '0':
			clear_screen()
			print(ascii_art('Au revoir!'))
			time.sleep(3)
			clear_screen()
			break
		else:
			print('Choix invalide.')
			input('Appuyez sur Entrée pour revenir au menu...')

if __name__ == '__main__':
	menu()



