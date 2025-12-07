import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QPushButton, QLineEdit
from PyQt5 import uic
from videoclub import FenetrePrincipale

identifiants = {
    "Cassette": {"password": "admin111", "access": "total"},
    "Bobinette": {"password": "rewind99", "access": "lecture"},
    "VHSinator": {"password": "beKindRewind", "access": "lecture"},
    "Pixel": {"password": "8bitpower", "access": "lecture"},
    "Comptable": {"password": "comptabilite", "access": "total"},
    "Stagiaire": {"password": "temp1111", "access": "lecture"}
}

class FenetreLogin(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("login.ui", self)
        self.setupUi()
        self.show()

    def setupUi(self):
        self.txtNomUtilisateur = self.findChild(QLineEdit, "txtNomUtilisateur")
        self.txtMotDePasse = self.findChild(QLineEdit, "txtMotDePasse")
        if self.txtMotDePasse:
            self.txtMotDePasse.setEchoMode(QLineEdit.Password)

        self.btnConnexion = self.findChild(QPushButton, "btnConnexion")
        if self.btnConnexion:
            self.btnConnexion.clicked.connect(self.se_connecter)

        self.btnFermer = self.findChild(QPushButton, "btnFermer")
        if self.btnFermer:
            self.btnFermer.clicked.connect(self.fermer_application)

        self.fenetre_principale = None

    def se_connecter(self):
        nom_utilisateur = self.txtNomUtilisateur.text().strip()
        mot_de_passe = self.txtMotDePasse.text().strip()

        if nom_utilisateur in identifiants and identifiants[nom_utilisateur]["password"] == mot_de_passe:
            self.ouvrir_fenetre_principale(identifiants[nom_utilisateur]["access"])
        else:
            QMessageBox.warning(self, "Erreur de connexion", "Mauvais identifiant, on se connait?")

    def ouvrir_fenetre_principale(self, access_type):
        try:
            if self.fenetre_principale is None:
                self.fenetre_principale = FenetrePrincipale(access_type)
            self.fenetre_principale.show()
            self.hide()
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Impossible d'ouvrir la fenêtre principale:\n{e}")

    def fermer_application(self):
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    fenetre = FenetreLogin()
    sys.exit(app.exec_())
