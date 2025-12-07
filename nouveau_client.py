from PyQt5.QtWidgets import QDialog, QLineEdit, QComboBox, QPushButton, QMessageBox, QDateEdit
from PyQt5 import uic
from fonctions import clients, add_client, update_client, Client, CarteCredit
from PyQt5.QtCore import QDate
from datetime import datetime

class FenetreNouveauClient(QDialog):
    def __init__(self, edit_index=None):
        super().__init__()
        uic.loadUi("nouveau_client.ui", self)
        self.edit_index = edit_index
        self.setupUi()

    def setupUi(self):
        # Champs client
        self.txtNom = self.findChild(QLineEdit, "txtNom")
        self.txtPrenom = self.findChild(QLineEdit, "txtPrenom")
        self.txtCourriel = self.findChild(QLineEdit, "txtCourriel")
        self.cmbSexe = self.findChild(QComboBox, "cmbSexe")
        self.txtPassword = self.findChild(QLineEdit, "txtPassword")
        self.dateInscription = self.findChild(QDateEdit, "dateInscription")

        # Champs cartes de crédit (2 cartes)
        self.txtNum1 = self.findChild(QLineEdit, "txtNum1")
        self.txtExpire1 = self.findChild(QLineEdit, "txtExpire1")
        self.txtCVV1 = self.findChild(QLineEdit, "txtCVV1")

        self.txtNum2 = self.findChild(QLineEdit, "txtNum2")
        self.txtExpire2 = self.findChild(QLineEdit, "txtExpire2")
        self.txtCVV2 = self.findChild(QLineEdit, "txtCVV2")

        # Boutons
        self.btnEnregistrer = self.findChild(QPushButton, "btnEnregistrer")
        self.btnAnnuler = self.findChild(QPushButton, "btnAnnuler")
        self.btnEnregistrer.clicked.connect(self.enregistrer_client)
        self.btnAnnuler.clicked.connect(self.reject)

        # Date du jour automatique si création
        if self.edit_index is None:
            self.dateInscription.setDate(QDate.currentDate())
            self.dateInscription.setReadOnly(True)

        # Préremplissage si modification
        if self.edit_index is not None:
            client = clients[self.edit_index]
            self.txtNom.setText(client.getNom())
            self.txtPrenom.setText(client.getPrenom())
            self.txtCourriel.setText(client.getCourriel())
            self.cmbSexe.setCurrentText(client.getSexe())
            self.txtPassword.setText(client.password)

            cartes = client.getCartes()
            if len(cartes) > 0:
                self.txtNum1.setText(cartes[0].numero)
                self.txtExpire1.setText(cartes[0].expiration)
                self.txtCVV1.setText(cartes[0].cvv)
            if len(cartes) > 1:
                self.txtNum2.setText(cartes[1].numero)
                self.txtExpire2.setText(cartes[1].expiration)
                self.txtCVV2.setText(cartes[1].cvv)

            self.dateInscription.setDate(datetime.strptime(client.getDateInscription(), "%d-%m-%Y").date())

    def enregistrer_client(self):
        nom = self.txtNom.text().strip()
        prenom = self.txtPrenom.text().strip()
        courriel = self.txtCourriel.text().strip()
        sexe = self.cmbSexe.currentText()
        password = self.txtPassword.text().strip()
        date_inscription = self.dateInscription.date().toString("dd-MM-yyyy")

        # Validation champs obligatoires
        if not nom or not prenom or not courriel:
            QMessageBox.warning(self, "Champs obligatoires", "Veuillez remplir le nom, prénom et courriel.")
            return
        if len(password) < 8:
            QMessageBox.warning(self, "Mot de passe", "Le mot de passe doit contenir au moins 8 caractères.")
            return
        for i, c in enumerate(clients):
            if c.getCourriel() == courriel and (self.edit_index is None or self.edit_index != i):
                QMessageBox.warning(self, "Courriel existant", "Ce courriel est déjà utilisé par un autre client.")
                return

        # Récupération des cartes depuis les lineEdit
        cartes = []
        if self.txtNum1.text().strip() and self.txtExpire1.text().strip() and self.txtCVV1.text().strip():
            cartes.append(CarteCredit(self.txtNum1.text().strip(),
                                      self.txtExpire1.text().strip(),
                                      self.txtCVV1.text().strip()))
        if self.txtNum2.text().strip() and self.txtExpire2.text().strip() and self.txtCVV2.text().strip():
            cartes.append(CarteCredit(self.txtNum2.text().strip(),
                                      self.txtExpire2.text().strip(),
                                      self.txtCVV2.text().strip()))

        client = Client(nom, prenom, courriel, sexe, date_inscription, cartes, password)

        try:
            if self.edit_index is None:
                add_client(client)
                QMessageBox.information(self, "Succès", f"Client {prenom} {nom} ajouté.")
            else:
                update_client(self.edit_index, client)
                QMessageBox.information(self, "Succès", f"Client {prenom} {nom} modifié.")
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Impossible d'enregistrer le client:\n{e}")