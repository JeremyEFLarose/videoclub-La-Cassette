from PyQt5.QtWidgets import QDialog, QLineEdit, QComboBox, QPushButton, QMessageBox, QDateEdit
from PyQt5 import uic
from fonctions import clients, add_client, update_client, find_client_name, Client, CarteCredit
from datetime import datetime
from PyQt5.QtCore import QDate
from PyQt5.QtGui import QIntValidator

class FenetreNouveauClient(QDialog):
    def __init__(self, edit_index=None):
        super().__init__()
        uic.loadUi("nouveau_client.ui", self)
        self.edit_index = edit_index
        self.setupUi()

    def setupUi(self):
        # Champs
        self.txtNom = self.findChild(QLineEdit, "txtNom")
        self.txtPrenom = self.findChild(QLineEdit, "txtPrenom")
        self.txtCourriel = self.findChild(QLineEdit, "txtCourriel")
        self.cmbSexe = self.findChild(QComboBox, "cmbSexe")
        self.txtPassword = self.findChild(QLineEdit, "txtPassword")
        self.dateInscription = self.findChild(QDateEdit, "dateInscription")

        # Carte de crédit
        self.txtNumCarte = self.findChild(QLineEdit, "txtNumCarte")
        self.txtExpire = self.findChild(QLineEdit, "txtExpire")
        self.txtCVV = self.findChild(QLineEdit, "txtCVV")

        # Boutons
        self.btnEnregistrer = self.findChild(QPushButton, "btnEnregistrer")
        self.btnAnnuler = self.findChild(QPushButton, "btnAnnuler")
        self.btnEnregistrer.clicked.connect(self.enregistrer_client)
        self.btnAnnuler.clicked.connect(self.reject)  # Ferme le dialog

        # --- Date du jour automatique ---
        if self.edit_index is None:
            self.dateInscription.setDate(QDate.currentDate())
            self.dateInscription.setReadOnly(True)

        # --- CVV : format obligatoire 2 chiffres / 2 chiffres ---
        # On peut forcer uniquement les chiffres et max 5 caractères (ex: "12/34")
        self.txtCVV.setMaxLength(5)
        self.txtCVV.setInputMask("00/00")  # Forme fixe 2 chiffres / 2 chiffres

        # Préremplissage si modification
        if self.edit_index is not None:
            client = clients[self.edit_index]
            self.txtNom.setText(client.getNom())
            self.txtPrenom.setText(client.getPrenom())
            self.txtCourriel.setText(client.getCourriel())
            self.cmbSexe.setCurrentText(client.getSexe())
            self.txtPassword.setText(client.password)
            if client.getCartes():
                carte = client.getCartes()[0]  # On prend la première carte
                self.txtNumCarte.setText(carte.numero)
                self.txtExpire.setText(carte.expiration)
                self.txtCVV.setText(carte.cvv)
            # La date originale reste modifiable si on modifie
            self.dateInscription.setDate(datetime.strptime(client.getDateInscription(), "%d-%m-%Y").date())

    def enregistrer_client(self):
        nom = self.txtNom.text().strip()
        prenom = self.txtPrenom.text().strip()
        courriel = self.txtCourriel.text().strip()
        sexe = self.cmbSexe.currentText()
        password = self.txtPassword.text().strip()
        date_inscription = self.dateInscription.date().toString("dd-MM-yyyy")

        num_carte = self.txtNumCarte.text().strip()
        expire = self.txtExpire.text().strip()
        cvv = self.txtCVV.text().strip()

        # Validation champs obligatoires
        if not nom or not prenom or not courriel:
            QMessageBox.warning(self, "Champs obligatoires", "Veuillez remplir le nom, prénom et courriel.")
            return

        if len(password) < 8:
            QMessageBox.warning(self, "Mot de passe", "Le mot de passe doit contenir au moins 8 caractères.")
            return

        # Vérification du courriel unique
        for i, c in enumerate(clients):
            if c.getCourriel() == courriel and (self.edit_index is None or self.edit_index != i):
                QMessageBox.warning(self, "Courriel existant", "Ce courriel est déjà utilisé par un autre client.")
                return

        # Création de la carte de crédit
        cartes = []
        if num_carte and expire and cvv:
            cartes.append(CarteCredit(num_carte, expire, cvv))

        client = Client(nom, prenom, courriel, sexe, date_inscription, cartes, password)

        try:
            if self.edit_index is None:
                add_client(client)
                QMessageBox.information(self, "Succès", f"Client {prenom} {nom} ajouté.")
            else:
                update_client(self.edit_index, client)
                QMessageBox.information(self, "Succès", f"Client {prenom} {nom} modifié.")

            self.accept()  # Ferme le dialog
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Impossible d'enregistrer le client:\n{e}")
