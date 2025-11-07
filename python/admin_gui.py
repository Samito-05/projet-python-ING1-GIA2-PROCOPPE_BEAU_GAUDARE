from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QLabel, QMessageBox
)
from PyQt6.QtCore import Qt

from python.admin_functions import (
    gui_add_movie,
    gui_add_room,
    gui_add_representation,
    gui_assign_representation_to_room
)

class AdminMenu(QWidget):
    def __init__(self, admin_user):
        super().__init__()
        self.admin_user = admin_user
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        title = QLabel(f"Administration - {self.admin_user.prenom} {self.admin_user.nom} (role={self.admin_user.role})")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        btn_add_movie = QPushButton("Ajouter un film")
        btn_add_movie.clicked.connect(gui_add_movie)
        layout.addWidget(btn_add_movie)

        btn_add_room = QPushButton("Ajouter une salle")
        btn_add_room.clicked.connect(gui_add_room)
        layout.addWidget(btn_add_room)

        btn_add_rep = QPushButton("Ajouter une représentation")
        btn_add_rep.clicked.connect(gui_add_representation)
        layout.addWidget(btn_add_rep)

        btn_assign = QPushButton("Attribuer une représentation à une salle")
        btn_assign.clicked.connect(gui_assign_representation_to_room)
        layout.addWidget(btn_assign)

        btn_back = QPushButton("Retour")
        btn_back.clicked.connect(self.close)
        layout.addWidget(btn_back)

        self.setLayout(layout)
        self.setWindowTitle("Panneau d'administration")
        self.setFixedSize(400, 260)
