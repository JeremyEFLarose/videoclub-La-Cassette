# fonctions.py

# -------------------- Classes --------------------
class CarteCredit:
    def __init__(self, numero, expiration, cvv):
        self.numero = numero
        self.expiration = expiration
        self.cvv = cvv


class Personne:
    def __init__(self, nom, prenom, sexe):
        self.nom = nom
        self.prenom = prenom
        self.sexe = sexe

    def getNom(self):
        return self.nom

    def getPrenom(self):
        return self.prenom

    def getSexe(self):
        return self.sexe


class Client(Personne):
    def __init__(self, nom, prenom, courriel, sexe, date_inscription, cartes=None, password=""):
        super().__init__(nom, prenom, sexe)
        self.courriel = courriel
        self.date_inscription = date_inscription
        self.password = password
        self.cartes = cartes if cartes else []

    def getCourriel(self):
        return self.courriel

    def getDateInscription(self):
        return self.date_inscription

    def getCartes(self):
        return self.cartes


class Film:
    def __init__(self, nom, duree, categories=None, acteurs=None):
        self.nom = nom
        self.duree = duree
        # S'assurer que categories est toujours une liste
        if isinstance(categories, str):
            self.categories = [cat.strip() for cat in categories.split(",")]
        else:
            self.categories = categories if categories else []
        # S'assurer que acteurs est toujours une liste
        self.acteurs = acteurs if acteurs else []

    def getNom(self):
        return self.nom

    def getDuree(self):
        return self.duree

    def getCategorie(self):
        """Retourne une chaîne avec les catégories séparées par virgule"""
        return ", ".join(self.categories)

    def getActeurs(self):
        """Retourne une chaîne avec les noms des acteurs séparés par virgule"""
        return ", ".join(self.acteurs)


# -------------------- Listes globales --------------------
clients = []

films = [
    Film("Troll", "2h28", ["Action", "Science-Fiction"], ["Tom Hanks", "Emma Watson"]),
    Film("Gladiateur", "1h47", ["Drame", "Action"], ["Russell Crowe", "Joaquin Phoenix"]),
    Film("Effet papillon", "3h01", ["Drame", "Psychologique", "Science-Fiction"], ["Ashton Kutcher"]),
    Film("Forrest Gump", "2h22", ["Drame", "Comédie"], ["Tom Hanks"]),
    Film("Her", "2h06", ["Romantique", "Comédie"], ["Joaquin Phoenix", "Scarlett Johansson"])
]


# -------------------- Clients --------------------
def add_client(client):
    clients.append(client)
    sauvegarder_clients()


def update_client(index, client):
    if 0 <= index < len(clients):
        clients[index] = client
        sauvegarder_clients()


def delete_client(index):
    if 0 <= index < len(clients):
        clients.pop(index)
        sauvegarder_clients()


def find_client_name(nom, prenom):
    for i, client in enumerate(clients):
        if client.getNom() == nom and client.getPrenom() == prenom:
            return i
    return -1


# -------------------- Films --------------------
def add_film(film):
    films.append(film)
    sauvegarder_films()


def update_film(index, film):
    if 0 <= index < len(films):
        films[index] = film
        sauvegarder_films()


def delete_film(index):
    if 0 <= index < len(films):
        films.pop(index)
        sauvegarder_films()


# -------------------- Sauvegarde optionnelle --------------------
def sauvegarder_clients():
    try:
        with open("clients.txt", "w", encoding="utf-8") as f:
            for c in clients:
                cartes_str = "|".join([f"{carte.numero},{carte.expiration},{carte.cvv}" for carte in c.getCartes()])
                f.write(f"{c.getNom()};{c.getPrenom()};{c.getCourriel()};{c.getSexe()};{c.getDateInscription()};{c.password};{cartes_str}\n")
    except Exception as e:
        print(f"Erreur sauvegarde clients: {e}")


def sauvegarder_films():
    try:
        with open("films.txt", "w", encoding="utf-8") as f:
            for film in films:
                categories_str = "|".join(film.categories)
                acteurs_str = "|".join(film.acteurs)
                f.write(f"{film.getNom()};{film.getDuree()};{categories_str};{acteurs_str}\n")
    except Exception as e:
        print(f"Erreur sauvegarde films: {e}")
