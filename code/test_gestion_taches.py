"""Tests unitaires du prototype : exécuter python -m unittest -v."""
from datetime import date, timedelta
import json
from pathlib import Path
import tempfile
import unittest
from gestion_taches import GestionTaches, ErreurValidation, ErreurDonnees


class TestsGestionTaches(unittest.TestCase):
    def setUp(self):
        self.dossier = tempfile.TemporaryDirectory()
        self.fichier = Path(self.dossier.name) / 'taches.json'
        self.jour = date(2026, 11, 14)
        self.g = GestionTaches(self.fichier, aujourdhui=self.jour)

    def tearDown(self):
        self.dossier.cleanup()

    def test_01_ajout_normal(self):
        t = self.g.ajouter('Dissertation', 'Français', '2026-11-20')
        self.assertEqual(t['titre'], 'Dissertation')
        self.assertFalse(t['terminee'])

    def test_02_persistance_json(self):
        self.g.ajouter('Exercice', 'Math', '2026-11-20')
        self.assertEqual(len(GestionTaches(self.fichier).lister()), 1)

    def test_03_tri_date_croissante(self):
        self.g.ajouter('B', 'Cours', '2026-11-28')
        self.g.ajouter('A', 'Cours', '2026-11-18')
        self.assertEqual([t['titre'] for t in self.g.lister()], ['A', 'B'])

    def test_04_titre_vide_refuse(self):
        with self.assertRaises(ErreurValidation):
            self.g.ajouter('  ', 'Cours', '2026-11-20')

    def test_05_date_invalide_refusee(self):
        with self.assertRaises(ErreurValidation):
            self.g.ajouter('Travail', 'Cours', '2026-02-30')

    def test_06_longueur_limite_100(self):
        self.assertEqual(len(self.g.ajouter('X' * 100, 'Cours', '2026-11-20')['titre']), 100)
        with self.assertRaises(ErreurValidation):
            self.g.ajouter('X' * 101, 'Cours', '2026-11-20')

    def test_07_terminer_et_filtrer(self):
        t = self.g.ajouter('Examen', 'Math', '2026-11-20')
        self.g.basculer_terminee(t['id'])
        self.assertEqual(len(self.g.lister(statut='terminees')), 1)
        self.assertEqual(len(self.g.lister(statut='a_faire')), 0)

    def test_08_filtre_cours(self):
        self.g.ajouter('A', 'Python', '2026-11-20')
        self.g.ajouter('B', 'Français', '2026-11-21')
        self.assertEqual([t['titre'] for t in self.g.lister(cours='PYTHON')], ['A'])

    def test_09_modifier(self):
        t = self.g.ajouter('Ancien', 'Cours', '2026-11-20')
        self.g.modifier(t['id'], 'Nouveau', 'Cours', '2026-11-19')
        self.assertEqual(self.g.obtenir(t['id'])['titre'], 'Nouveau')

    def test_10_supprimer(self):
        t = self.g.ajouter('Travail', 'Cours', '2026-11-20')
        self.g.supprimer(t['id'])
        self.assertEqual(len(self.g.lister()), 0)

    def test_11_echeance_et_retard(self):
        t1 = self.g.ajouter('Urgent', 'Cours', '2026-11-16')
        t2 = self.g.ajouter('Passé', 'Cours', '2026-11-12')
        self.assertEqual(self.g.urgence(t1), 'À rendre bientôt')
        self.assertEqual(self.g.urgence(t2), 'En retard')

    def test_12_json_corrompu(self):
        self.fichier.write_text('{invalide', encoding='utf-8')
        with self.assertRaises(ErreurDonnees):
            self.g.lister()

    def test_13_id_inconnu_refuse(self):
        with self.assertRaises(ErreurValidation):
            self.g.basculer_terminee('absent')

    def test_14_booleen_json_incorrect_refuse(self):
        # Correction après revue : une chaîne "non" n'est pas un vrai booléen False.
        contenu = [{'id': 'A1', 'titre': 'Travail', 'cours': 'Python',
                    'date_limite': '2026-11-20', 'terminee': 'non'}]
        self.fichier.write_text(json.dumps(contenu), encoding='utf-8')
        with self.assertRaises(ErreurDonnees):
            self.g.lister()

    def test_15_date_corrompue_dans_json_refusee(self):
        contenu = [{'id': 'A1', 'titre': 'Travail', 'cours': 'Python',
                    'date_limite': '2026-02-30', 'terminee': False}]
        self.fichier.write_text(json.dumps(contenu), encoding='utf-8')
        with self.assertRaises(ErreurDonnees):
            self.g.lister()

    def test_16_id_duplique_json_refuse(self):
        tache = {'id': 'A1', 'titre': 'Travail', 'cours': 'Python',
                 'date_limite': '2026-11-20', 'terminee': False}
        self.fichier.write_text(json.dumps([tache, tache]), encoding='utf-8')
        with self.assertRaises(ErreurDonnees):
            self.g.lister()

    def test_17_filtre_statut_invalide(self):
        with self.assertRaises(ErreurValidation):
            self.g.lister(statut='inconnu')

    def test_18_reouvrir_tache(self):
        t = self.g.ajouter('Rapport', 'Python', '2026-11-20')
        self.g.basculer_terminee(t['id'])
        self.g.basculer_terminee(t['id'])
        self.assertFalse(self.g.obtenir(t['id'])['terminee'])


if __name__ == '__main__':
    unittest.main()
