from PyQt5.QtWidgets import QDialog, QLineEdit, QComboBox, QPushButton, QMessageBox, QDateEdit, QTableWidgetItem
from PyQt5 import uic
from fonctions import clients, add_client, update_client, Client, CarteCredit
from PyQt5.QtCore import QDate
from datetime import datetime
from PyQt5.QtWidgets import QTableWidget

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

        # Table pour cartes de crédit
        self.tableCartes = self.findChild(QTableWidget, "tableCartes")
        self.tableCartes.setColumnCount(3)
        self.tableCartes.setHorizontalHeaderLabels(["Numéro", "Expiration", "CVV"])
        self.tableCartes.setRowCount(2)  # Toujours 2 lignes pour 2 cartes max

        # Boutons
        self.btnEnregistrer = self.findChild(QPushButton, "btnEnregistrer")
        self.btnAnnuler = self.findChild(QPushButton, "btnAnnuler")
        self.btnEnregistrer.clicked.connect(self.enregistrer_client)
        self.btnAnnuler.clicked.connect(self.reject)

        # Date du jour automatisé
        if self.edit_index is None:
            self.dateInscription.setDate(QDate.currentDate())
            self.dateInscription.setReadOnly(True)

        # Retrouver les données si on modifie un client
        if self.edit_index is not None:
            client = clients[self.edit_index]
            self.txtNom.setText(client.getNom())
            self.txtPrenom.setText(client.getPrenom())
            self.txtCourriel.setText(client.getCourriel())
            self.cmbSexe.setCurrentText(client.getSexe())
            self.txtPassword.setText(client.password)

            # Récupérer les informations de la carte de crédit
            cartes = client.getCartes()
            for i, carte in enumerate(cartes):
                if i < 2:  # Max 2 cartes de crédit
                    self.tableCartes.setItem(i, 0, QTableWidgetItem(carte.numero))
                    self.tableCartes.setItem(i, 1, QTableWidgetItem(carte.expiration))
                    self.tableCartes.setItem(i, 2, QTableWidgetItem(carte.cvv))

            self.dateInscription.setDate(datetime.strptime(client.getDateInscription(), "%d-%m-%Y").date())

    def enregistrer_client(self):
        nom = self.txtNom.text().strip()
        prenom = self.txtPrenom.text().strip()
        courriel = self.txtCourriel.text().strip()
        sexe = self.cmbSexe.currentText()
        password = self.txtPassword.text().strip()
        date_inscription = self.dateInscription.date().toString("dd-MM-yyyy")

        # Champs obligatoires Nom, Prénom et Courriel
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

        # Récupération des cartes depuis la table
        cartes = []
        for row in range(self.tableCartes.rowCount()):
            num_item = self.tableCartes.item(row, 0)
            expire_item = self.tableCartes.item(row, 1)
            cvv_item = self.tableCartes.item(row, 2)
            if num_item and expire_item and cvv_item:
                num = num_item.text().strip()
                expire = expire_item.text().strip()
                cvv = cvv_item.text().strip()
                if num and expire and cvv:
                    cartes.append(CarteCredit(num, expire, cvv))

        # Création du client
        client = Client(nom, prenom, courriel, sexe, date_inscription, cartes, password)

        try:
            if self.edit_index is None:
                add_client(client)  # Ajouter un nouveau client
                QMessageBox.information(self, "Succès", f"Client {prenom} {nom} ajouté.")
            else:
                update_client(self.edit_index, client)  # Modifier un client existant
                QMessageBox.information(self, "Succès", f"Client {prenom} {nom} modifié.")
            self.accept()  # Ferme la fenêtre après enregistrement
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Impossible d'enregistrer le client:\n{e}")