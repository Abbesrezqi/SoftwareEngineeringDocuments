"""Logique métier du prototype Omnivox - suivi scolaire (soumission 2).
Aucun accès à la véritable plateforme Omnivox.
"""
from datetime import date, datetime
import json
import os
from pathlib import Path
import tempfile
from uuid import uuid4


class ErreurValidation(ValueError):
    """Entrée fournie invalide."""


class ErreurDonnees(Exception):
    """Fichier JSON absent de permissions ou corrompu."""


class GestionTaches:
    def __init__(self, chemin, aujourdhui=None):
        self.chemin = Path(chemin)
        self.aujourdhui = aujourdhui  # Date fixe facultative pour les tests.

    def _date_jour(self):
        return self.aujourdhui or date.today()

    def _lire(self):
        """Lit le fichier JSON et vérifie les champs de chaque tâche."""
        if not self.chemin.exists():
            return []
        try:
            with self.chemin.open('r', encoding='utf-8') as fichier:
                taches = json.load(fichier)
        except (OSError, UnicodeError, json.JSONDecodeError) as exc:
            raise ErreurDonnees("Impossible de lire le fichier de tâches (JSON invalide ou inaccessible).") from exc

        if not isinstance(taches, list):
            raise ErreurDonnees("Le fichier JSON doit contenir une liste de tâches.")

        identifiants = set()
        for tache in taches:
            if not isinstance(tache, dict):
                raise ErreurDonnees("Une tâche a un format incorrect dans le fichier JSON.")
            champs = ('id', 'titre', 'cours', 'date_limite', 'terminee')
            if not all(cle in tache for cle in champs):
                raise ErreurDonnees("Il manque un champ obligatoire dans le fichier JSON.")
            if not all(isinstance(tache[cle], str) and tache[cle].strip()
                       for cle in ('id', 'titre', 'cours', 'date_limite')):
                raise ErreurDonnees("Une tâche contient un texte vide ou un mauvais type de donnée.")
            if type(tache['terminee']) is not bool:
                raise ErreurDonnees("Le statut d'une tâche doit être vrai ou faux dans le JSON.")
            try:
                date.fromisoformat(tache['date_limite'])
            except ValueError as exc:
                raise ErreurDonnees("Une date du fichier JSON n'est pas valide.") from exc
            if tache['id'] in identifiants:
                raise ErreurDonnees("Deux tâches du fichier JSON possèdent le même identifiant.")
            identifiants.add(tache['id'])
        return taches

    def _ecrire(self, taches):
        """Sauvegarde d'abord dans un fichier temporaire, puis le remplace."""
        nom_temporaire = None
        try:
            self.chemin.parent.mkdir(parents=True, exist_ok=True)
            with tempfile.NamedTemporaryFile('w', encoding='utf-8', dir=self.chemin.parent,
                                             suffix='.tmp', delete=False) as temporaire:
                nom_temporaire = temporaire.name
                json.dump(taches, temporaire, ensure_ascii=False, indent=2)
            os.replace(nom_temporaire, self.chemin)
        except OSError as exc:
            raise ErreurDonnees("Enregistrement impossible. Vérifiez le dossier et ses permissions.") from exc
        finally:
            if nom_temporaire and os.path.exists(nom_temporaire):
                os.unlink(nom_temporaire)

    @staticmethod
    def _valider(titre, cours, date_limite):
        titre = str(titre or '').strip()
        cours = str(cours or '').strip()
        if not 1 <= len(titre) <= 100:
            raise ErreurValidation("Le titre est obligatoire (maximum 100 caractères).")
        if not 1 <= len(cours) <= 60:
            raise ErreurValidation("Le cours est obligatoire (maximum 60 caractères).")
        try:
            date_valide = date.fromisoformat(str(date_limite))
        except (TypeError, ValueError):
            raise ErreurValidation("La date limite doit être une date valide au format AAAA-MM-JJ.") from None
        return titre, cours, date_valide.isoformat()

    def ajouter(self, titre, cours, date_limite):
        titre, cours, date_limite = self._valider(titre, cours, date_limite)
        taches = self._lire()
        nouvelle = {
            'id': uuid4().hex[:12], 'titre': titre, 'cours': cours,
            'date_limite': date_limite, 'terminee': False,
            'cree_le': datetime.now().isoformat(timespec='seconds')
        }
        taches.append(nouvelle)
        self._ecrire(taches)
        return nouvelle

    def lister(self, cours='', statut='toutes'):
        if statut not in ('toutes', 'a_faire', 'terminees', 'urgentes'):
            raise ErreurValidation("Statut de filtre non reconnu.")
        taches = self._lire()
        if cours:
            taches = [t for t in taches if t['cours'].casefold() == cours.casefold()]
        if statut == 'a_faire':
            taches = [t for t in taches if not t['terminee']]
        elif statut == 'terminees':
            taches = [t for t in taches if t['terminee']]
        elif statut == 'urgentes':
            taches = [t for t in taches if self.urgence(t) in ('En retard', 'À rendre bientôt')]
        return sorted(taches, key=lambda t: (t['date_limite'], t['titre'].casefold()))

    def obtenir(self, identifiant):
        return next((t for t in self._lire() if t['id'] == identifiant), None)

    def modifier(self, identifiant, titre, cours, date_limite):
        titre, cours, date_limite = self._valider(titre, cours, date_limite)
        taches = self._lire()
        for tache in taches:
            if tache['id'] == identifiant:
                tache.update(titre=titre, cours=cours, date_limite=date_limite)
                self._ecrire(taches)
                return tache
        raise ErreurValidation("Tâche introuvable.")

    def basculer_terminee(self, identifiant):
        taches = self._lire()
        for tache in taches:
            if tache['id'] == identifiant:
                tache['terminee'] = not tache['terminee']
                self._ecrire(taches)
                return tache
        raise ErreurValidation("Tâche introuvable.")

    def supprimer(self, identifiant):
        taches = self._lire()
        reste = [t for t in taches if t['id'] != identifiant]
        if len(taches) == len(reste):
            raise ErreurValidation("Tâche introuvable.")
        self._ecrire(reste)

    def urgence(self, tache):
        if tache['terminee']:
            return 'Terminée'
        difference = (date.fromisoformat(tache['date_limite']) - self._date_jour()).days
        if difference < 0:
            return 'En retard'
        if difference <= 2:
            return 'À rendre bientôt'
        return 'À venir'

    def cours(self):
        return sorted({t['cours'] for t in self._lire()}, key=str.casefold)
