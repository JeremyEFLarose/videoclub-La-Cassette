from PyQt5.QtWidgets import QMainWindow, QTableWidget, QTableWidgetItem, QMessageBox, QPushButton
from PyQt5 import uic
from fonctions import clients, films, find_client_name, delete_client, delete_film
from nouveau_client import FenetreNouveauClient
from nouveau_film import FenetreNouveauFilm

class FenetrePrincipale(QMainWindow):
    def __init__(self, access_type="total"):
        super().__init__()
        uic.loadUi("videoclub.ui", self)
        self.access_type = access_type  # total ou lecture
        self.setupUi()
        self.refresh_table_clients()
        self.refresh_table_films()
        self.show()

    def setupUi(self):
        # Tables
        self.tableClients = self.findChild(QTableWidget, "tableClients")
        self.tableFilms = self.findChild(QTableWidget, "tableFilms")

        # Boutons pour Clients
        self.btnAjouterClient = self.findChild(QPushButton, "btnAjouterClient")
        self.btnModifier = self.findChild(QPushButton, "btnModifier")
        self.btnSupprimer = self.findChild(QPushButton, "btnSupprimer")

        # Boutons pour Films
        self.btnAjouterFilm = self.findChild(QPushButton, "btnAjouterFilm")

        # Bouton Déconnexion
        self.btnDeconnexion = self.findChild(QPushButton, "btnDeconnexion")

        # Liens des boutons
        self.btnAjouterClient.clicked.connect(self.ajouter_client)
        self.btnModifier.clicked.connect(self.modifier_client)
        self.btnSupprimer.clicked.connect(self.supprimer_selection)
        self.btnAjouterFilm.clicked.connect(self.ajouter_film)
        self.btnDeconnexion.clicked.connect(self.deconnexion)

        # Gestion des droits selon le type d'accès, seulement une restriction en lecture
        if self.access_type == "lecture":
            for btn in [self.btnAjouterClient, self.btnModifier, self.btnSupprimer, self.btnAjouterFilm]:
                btn.setEnabled(False)

    # ----- Rafraîchir tableaux -----
    def refresh_table_clients(self):
        self.tableClients.setRowCount(0)
        for c in clients:
            ligne = self.tableClients.rowCount()
            self.tableClients.insertRow(ligne)
            self.tableClients.setItem(ligne, 0, QTableWidgetItem(c.getNom()))
            self.tableClients.setItem(ligne, 1, QTableWidgetItem(c.getPrenom()))
            self.tableClients.setItem(ligne, 2, QTableWidgetItem(c.getCourriel()))

    def refresh_table_films(self):
        self.tableFilms.setRowCount(0)
        for f in films:
            ligne = self.tableFilms.rowCount()
            self.tableFilms.insertRow(ligne)

            itemNom = QTableWidgetItem(f.getNom())
            itemNom.setToolTip(f"Acteurs : {f.getActeurs()}")
            self.tableFilms.setItem(ligne, 0, itemNom)

            itemDuree = QTableWidgetItem(f.getDuree())
            itemDuree.setToolTip(f"Acteurs : {f.getActeurs()}")
            self.tableFilms.setItem(ligne, 1, itemDuree)

            itemCategorie = QTableWidgetItem(f.getCategorie())
            itemCategorie.setToolTip(f"Acteurs : {f.getActeurs()}")
            self.tableFilms.setItem(ligne, 2, itemCategorie)

    # ----- Clients -----
    def ajouter_client(self):
        dlg = FenetreNouveauClient()
        if dlg.exec_():
            self.refresh_table_clients()

    def modifier_client(self):
        ligne = self.tableClients.currentRow()
        if ligne == -1:
            QMessageBox.information(self, "Sélection requise", "Sélectionnez un client à modifier.")
            return
        nom = self.tableClients.item(ligne, 0).text()
        prenom = self.tableClients.item(ligne, 1).text()
        index = find_client_name(nom, prenom)
        dlg = FenetreNouveauClient(edit_index=index)
        if dlg.exec_():
            self.refresh_table_clients()

    # ----- Films ------
    def ajouter_film(self):
        dlg = FenetreNouveauFilm()
        if dlg.exec_():
            self.refresh_table_films()

    # ---- Supprimer -----
    def supprimer_selection(self):
        if self.tableClients.currentRow() != -1:
            ligne = self.tableClients.currentRow()
            nom = self.tableClients.item(ligne, 0).text()
            prenom = self.tableClients.item(ligne, 1).text()
            if QMessageBox.question(self, "Confirmer", f"Supprimer le client {prenom} {nom} ?") == QMessageBox.Yes:
                index = find_client_name(nom, prenom)
                if index != -1:
                    delete_client(index)
                    self.refresh_table_clients()
        elif self.tableFilms.currentRow() != -1:
            ligne = self.tableFilms.currentRow()
            titre = self.tableFilms.item(ligne, 0).text()
            if QMessageBox.question(self, "Confirmer", f"Supprimer le film '{titre}' ?") == QMessageBox.Yes:
                for i, f in enumerate(films):
                    if f.getNom() == titre:
                        delete_film(i)
                        break
                self.refresh_table_films()
        else:
            QMessageBox.information(self, "Aucun élément", "Sélectionnez un client ou un film à supprimer.")

    # ----- Déconnexion -----
    def deconnexion(self):
        try:
            from login import FenetreLogin  # Import local pour éviter les imports circulaires
            self.close()
            self.login = FenetreLogin()
            self.login.show()
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Impossible de se déconnecter:\n{e}")