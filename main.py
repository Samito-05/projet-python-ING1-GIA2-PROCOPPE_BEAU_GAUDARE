from PyQt6.QtWidgets import QApplication
from python.models import Film, Salle_info, Utilisateur
from python.visuals import ascii_art, clear_screen
from python.admin_gui import AdminMenu
from python.user_gui import UserMenu
from python.user_functions import list_films, buy_ticket
from python.qt_gui import MainMenu
import storage
import sys
import getpass
import time


if __name__ == "__main__":

    app = QApplication(sys.argv)

    # Make sure storage is imported before this point
    window = MainMenu(storage)
    window.show()

    sys.exit(app.exec())



