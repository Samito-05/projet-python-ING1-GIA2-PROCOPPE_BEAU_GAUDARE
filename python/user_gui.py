from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
from PyQt6.QtCore import Qt
from python.user_functions import list_films, buy_ticket

class UserMenu(QWidget):
    def __init__(self, user):
        super().__init__()
        self.user = user
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        title = QLabel(f"Menu Utilisateur - {self.user.prenom} {self.user.nom} (role={self.user.role})")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        btn_films = QPushButton("Voir les films disponibles")
        btn_films.clicked.connect(list_films)
        layout.addWidget(btn_films)

        btn_ticket = QPushButton("Réserver une salle")
        btn_ticket.clicked.connect(buy_ticket)
        layout.addWidget(btn_ticket)

        btn_back = QPushButton("Retour")
        btn_back.clicked.connect(self.close)
        layout.addWidget(btn_back)

        self.setLayout(layout)
        self.setWindowTitle("Menu Utilisateur")
        self.setFixedSize(350, 220)
