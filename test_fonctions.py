import unittest
from fonctions import Client, Film, clients, films, add_client, update_client, find_client_name

class TestFonctionsVideoclub(unittest.TestCase):

#Vider les listes avant chaque tests
    def setUp(self):
        clients.clear()
        films.clear()

    # ----- Tests Clients -----
    def test_ajout_client(self):
        c = Client("Dupont", "Jean", "jean.dupont@test.com", "M", "06-12-2025")
        add_client(c)
        self.assertIn(c, clients)
        self.assertEqual(len(clients), 1)

    def test_modification_client(self):
        c = Client("Dupont", "Jean", "jean.dupont@test.com", "M", "06-12-2025")
        add_client(c)
        c_modifie = Client("Dupont", "Jean", "jean.dupont@test.com", "M", "06-12-2025", password="12345678")
        update_client(0, c_modifie)
        self.assertEqual(clients[0].password, "12345678")

    def test_recherche_client(self):
        c = Client("Dupont", "Jean", "jean.dupont@test.com", "M", "06-12-2025")
        add_client(c)
        index = find_client_name("Dupont", "Jean")
        self.assertEqual(index, 0)

    # ----- Tests Films -----
    def test_ajout_film(self):
        f = Film("Inception", "2h28", ["Science-Fiction"], ["Leonardo DiCaprio"])
        films.append(f)  # Utilise append directement si tu veux éviter la sauvegarde
        self.assertIn(f, films)
        self.assertEqual(len(films), 1)
        self.assertEqual(f.getNom(), "Inception")
        self.assertEqual(f.getCategorie(), "Science-Fiction")
        self.assertEqual(f.getActeurs(), "Leonardo DiCaprio")

    def test_multiple_acteurs(self):
        f = Film("Her", "2h06", ["Romantique", "Comédie"], ["Joaquin Phoenix", "Scarlett Johansson"])
        films.append(f)
        self.assertEqual(f.getActeurs(), "Joaquin Phoenix, Scarlett Johansson")
        self.assertEqual(f.getCategorie(), "Romantique, Comédie")

if __name__ == "__main__":
    unittest.main()