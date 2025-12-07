from PyQt5.QtWidgets import QDialog, QLineEdit, QPushButton, QMessageBox
from PyQt5 import uic
from fonctions import films, add_film, update_film, Film

class FenetreNouveauFilm(QDialog):
    def __init__(self, edit_index=None):
        super().__init__()
        uic.loadUi("nouveau_film.ui", self)  # Charge l’UI
        self.edit_index = edit_index
        self.setupUi()

    def setupUi(self):
        # Champs
        self.txtTitre = self.findChild(QLineEdit, "txtTitre")
        self.txtDuree = self.findChild(QLineEdit, "txtDuree")
        self.txtCategorie = self.findChild(QLineEdit, "txtCategorie")  # Singulier

        # Boutons
        self.btnEnregistrer = self.findChild(QPushButton, "btnEnregistrer")
        self.btnAnnuler = self.findChild(QPushButton, "btnAnnuler")

        self.btnEnregistrer.clicked.connect(self.enregistrer_film)
        self.btnAnnuler.clicked.connect(self.reject)  # Ferme seulement le dialog

        # Préremplissage si modification
        if self.edit_index is not None:
            film = films[self.edit_index]
            self.txtTitre.setText(film.getNom())
            self.txtDuree.setText(film.getDuree())
            self.txtCategorie.setText(film.getCategorie())

    def enregistrer_film(self):
        titre = self.txtTitre.text().strip()
        duree = self.txtDuree.text().strip()
        categorie = self.txtCategorie.text().strip()

        # Validation
        if not titre or not duree:
            QMessageBox.warning(self, "Champs obligatoires",
                                "Veuillez remplir au minimum le titre et la durée.")
            return

        try:
            film = Film(titre, duree, categorie)
            if self.edit_index is None:
                add_film(film)  # Ajoute dans films et sauvegarde
                QMessageBox.information(self, "Succès", f"Film '{titre}' ajouté.")
            else:
                update_film(self.edit_index, film)
                QMessageBox.information(self, "Succès", f"Film '{titre}' modifié.")
            self.accept()  # Ferme le dialog
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Impossible d’enregistrer le film:\n{e}")
