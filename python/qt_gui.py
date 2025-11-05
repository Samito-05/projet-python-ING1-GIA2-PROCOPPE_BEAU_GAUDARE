from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QMessageBox, QInputDialog, QApplication, QLineEdit
)
from PyQt6.QtCore import Qt
import sys
import storage
from python.user_gui import UserMenu
# from admin_menu_gui import AdminMenu  # when you convert admin menu

class MainMenu(QWidget):
    def __init__(self, storage):
        super().__init__()
        self.storage = storage
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        btn_films = QPushButton("Afficher les films")
        btn_films.clicked.connect(self.show_films)
        layout.addWidget(btn_films)

        btn_login = QPushButton("Se connecter")
        btn_login.clicked.connect(self.login_user)
        layout.addWidget(btn_login)

        btn_create = QPushButton("Créer un compte utilisateur")
        btn_create.clicked.connect(self.create_user)
        layout.addWidget(btn_create)

        btn_admin = QPushButton("Accéder au panneau d'administration")
        btn_admin.clicked.connect(self.login_admin)
        layout.addWidget(btn_admin)

        btn_quit = QPushButton("Quitter")
        btn_quit.clicked.connect(self.close)
        layout.addWidget(btn_quit)

        self.setLayout(layout)
        self.setWindowTitle("CY-NEMA APP")
        self.setFixedSize(350, 300)
        self.show()

    def show_films(self):
        films = self.storage.list_films()
        if not films:
            QMessageBox.information(self, "Films", "Aucun film.")
            return
        msg = ""
        for f in films:
            msg += f"- {f.titre}: {f.duree}min [{f.categorie}] (Age min={f.age_min})\n"
        QMessageBox.information(self, "Films disponibles", msg)

    def login_user(self):
        email, ok = QInputDialog.getText(self, "Connexion", "Email :")
        if not ok or not email:
            return
        pwd, ok = QInputDialog.getText(self, "Connexion", "Mot de passe :", echo=QLineEdit.EchoMode.Password)
        if not ok:
            return

        u = self.storage.authenticate_user(email, pwd)
        if u:
            QMessageBox.information(self, "Bienvenue", f"{u.prenom} {u.nom}")
            win = UserMenu(u)
            win.show()
        else:
            QMessageBox.warning(self, "Erreur", "Identifiants invalides.")

    def create_user(self):
        nom, ok = QInputDialog.getText(self, "Création", "Nom :")
        if not ok or not nom:
            return
        prenom, ok = QInputDialog.getText(self, "Création", "Prénom :")
        if not ok or not prenom:
            return
        dob, ok = QInputDialog.getText(self, "Création", "Date de naissance (YYYY-MM-DD) :")
        if not ok or not dob:
            return
        email, ok = QInputDialog.getText(self, "Création", "Email :")
        if not ok or not email:
            return
        pwd, ok = QInputDialog.getText(self, "Création", "Mot de passe :", echo=QLineEdit.EchoMode.Password)
        if not ok:
            return

        try:
            u = self.storage.create_user(nom=nom, prenom=prenom, date_naissance=dob, email=email, password=pwd)
            QMessageBox.information(self, "Compte créé", f"{u.email} créé.")
            win = UserMenu(u)
            win.show()
        except ValueError as e:
            QMessageBox.warning(self, "Erreur", str(e))

    def login_admin(self):
        email, ok = QInputDialog.getText(self, "Admin", "Email :")
        if not ok or not email:
            return
        pwd, ok = QInputDialog.getText(self, "Admin", "Mot de passe :", echo=QLineEdit.EchoMode.Password)
        if not ok:
            return

        u = self.storage.authenticate_admin(email, pwd)
        if u:
            QMessageBox.information(self, "Bienvenue", f"{u.prenom} {u.nom} (Admin)")
            # win = AdminMenu(u)  # once admin menu GUI exists
            # win.show()
        else:
            QMessageBox.warning(self, "Erreur", "Identifiants invalides.")