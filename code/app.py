"""Petit serveur web HTTP local en Python standard. Aucun paquet externe requis.
Lancer : python app.py, puis ouvrir http://127.0.0.1:8000
"""
from html import escape
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
import os
from urllib.parse import parse_qs, quote, urlsplit
from gestion_taches import GestionTaches, ErreurValidation, ErreurDonnees

BASE = Path(__file__).resolve().parent
CHEMIN_DONNEES = Path(os.environ.get('OMNIVOX_TACHES_JSON', str(BASE / 'data' / 'taches.json')))
gestion = GestionTaches(CHEMIN_DONNEES)

STYLE = """<style>
:root{color-scheme:light}*{box-sizing:border-box}body{font-family:system-ui,Arial,sans-serif;background:#f3f6fb;margin:0;color:#172b4d}
header{background:#173d78;color:white;padding:26px 5%}header h1{margin:0;font-size:26px}header p{margin:6px 0 0;opacity:.87}
main{width:min(1100px,94%);margin:24px auto}.grille{display:grid;grid-template-columns:300px 1fr;gap:22px}
section{background:white;border:1px solid #dce4ef;border-radius:12px;padding:20px;margin-bottom:18px;box-shadow:0 3px 14px #192e5210}
h2{margin-top:0;font-size:19px}label{display:block;font-size:13px;font-weight:700;margin:12px 0 5px}
input,select{width:100%;padding:11px;border:1px solid #b8c9dd;border-radius:7px;background:#fff;font:inherit}
button,.bouton{background:#1754a7;color:white;border:0;border-radius:7px;padding:10px 13px;font:inherit;cursor:pointer;text-decoration:none;display:inline-block}
button:hover,.bouton:hover{background:#0f3a75}.petit{font-size:12px;padding:7px 10px}.gris{background:#536783}.rouge{background:#af2d38}
form.enligne{display:inline-block;margin-right:4px}table{border-collapse:collapse;width:100%}td,th{text-align:left;padding:12px 8px;border-bottom:1px solid #e4eaf3;font-size:14px;vertical-align:middle}th{background:#f5f8fd}
.etiquette{display:inline-block;border-radius:100px;padding:4px 9px;font-size:12px;font-weight:700;background:#e6eefa}
.retard{background:#ffe2e6;color:#8c1427}.urgent{background:#ffedca;color:#7b5200}.terminee{background:#d8f6e9;color:#116142}
.message{background:#fff2df;border-left:4px solid #e19a21;padding:13px;border-radius:5px;margin-bottom:16px}
.pied{font-size:12px;color:#536783;margin:18px 0}a{color:#1754a7}td.actions{min-width:240px}
@media(max-width:800px){.grille{grid-template-columns:1fr}table,thead,tbody,tr,td,th{display:block}thead{display:none}tr{border:1px solid #dce4ef;margin-bottom:10px}td{border:0;padding:8px}}
</style>"""


def html_page(contenu, titre='Suivi scolaire'):
    return ("<!doctype html><html lang='fr'><head><meta charset='utf-8'><meta name='viewport' "
            "content='width=device-width,initial-scale=1'><title>" + escape(titre) + "</title>" + STYLE + "</head><body>"
            "<header><h1>Omnivox · Simplification du suivi scolaire</h1><p>Prototype pédagogique indépendant — sans connexion à Omnivox</p></header>"
            "<main>" + contenu + "<p class='pied'>Projet de session • Langage de script • Abbes Rezqi et Ali Rechachi</p></main></body></html>")


def afficher_accueil(filtre_cours='', filtre_statut='toutes', message=''):
    taches = gestion.lister(filtre_cours, filtre_statut)
    cours = gestion.cours()
    choix_cours = "<option value=''>Tous les cours</option>" + ''.join(
        f"<option value='{escape(c, quote=True)}' {'selected' if c == filtre_cours else ''}>{escape(c)}</option>" for c in cours)
    statuts = [('toutes','Toutes'),('a_faire','À faire'),('terminees','Terminées'),('urgentes','Urgentes / en retard')]
    choix_statut = ''.join(f"<option value='{s}' {'selected' if filtre_statut == s else ''}>{escape(n)}</option>" for s,n in statuts)
    formulaire = """<section><h2>Ajouter un travail</h2><form method='post' action='/ajouter'>
    <label for='titre'>Titre du travail</label><input id='titre' name='titre' maxlength='100' required placeholder='Ex. Dissertation finale'>
    <label for='cours'>Cours</label><input id='cours' name='cours' maxlength='60' required placeholder='Ex. Français'>
    <label for='date_limite'>Date limite</label><input id='date_limite' type='date' name='date_limite' required>
    <p><button type='submit'>Ajouter la tâche</button></p></form></section>"""
    lignes=[]
    for t in taches:
        identifiant = escape(t['id'], quote=True)
        etat = gestion.urgence(t)
        classe = 'terminee' if t['terminee'] else ('retard' if etat == 'En retard' else ('urgent' if etat == 'À rendre bientôt' else ''))
        lignes.append(f"<tr><td><strong>{escape(t['titre'])}</strong></td><td>{escape(t['cours'])}</td><td>{escape(t['date_limite'])}</td>"
                      f"<td><span class='etiquette {classe}'>{escape(etat)}</span></td>"
                      f"<td class='actions'><form method='post' action='/terminer' class='enligne'><input type='hidden' name='id' value='{identifiant}'>"
                      f"<button class='petit' type='submit'>{'Réouvrir' if t['terminee'] else 'Terminer'}</button></form>"
                      f"<a class='bouton petit gris' href='/modifier?id={quote(t['id'])}'>Modifier</a> "
                      f"<form method='post' action='/supprimer' class='enligne'><input type='hidden' name='id' value='{identifiant}'>"
                      "<button class='petit rouge' type='submit' onclick='return confirm(&quot;Supprimer ce travail ?&quot;)'>Supprimer</button></form></td></tr>")
    tableau = "<table><thead><tr><th>Travail</th><th>Cours</th><th>Échéance</th><th>Indicateur</th><th>Actions</th></tr></thead><tbody>" + ''.join(lignes) + "</tbody></table>" if lignes else "<p>Aucune tâche trouvée. Ajoute ton premier travail ou change les filtres.</p>"
    bloc = ("<section><h2>Travaux et échéances</h2><form method='get' action='/'>"
            "<div style='display:grid;grid-template-columns:1fr 1fr;gap:10px'>"
            f"<div><label>Filtrer par cours</label><select name='cours'>{choix_cours}</select></div>"
            f"<div><label>Filtrer par statut</label><select name='statut'>{choix_statut}</select></div></div>"
            "<p><button class='petit' type='submit'>Appliquer les filtres</button> <a href='/'>Effacer</a></p></form>"
            f"<p>{len(taches)} travail(aux) affiché(s) • tri par date limite croissante</p>{tableau}</section>")
    avertissement = f"<div class='message'>{escape(message)}</div>" if message else ''
    return html_page(avertissement + '<div class="grille"><div>'+formulaire+'</div><div>'+bloc+'</div></div>')


def afficher_modification(tache):
    if not tache:
        raise ErreurValidation('Tâche introuvable.')
    identifiant = escape(tache['id'], quote=True)
    contenu = f"""<section><h2>Modifier un travail</h2><form method='post' action='/modifier'>
    <input type='hidden' name='id' value='{identifiant}'>
    <label>Titre</label><input name='titre' maxlength='100' value='{escape(tache['titre'], quote=True)}' required>
    <label>Cours</label><input name='cours' maxlength='60' value='{escape(tache['cours'], quote=True)}' required>
    <label>Date limite</label><input type='date' name='date_limite' value='{escape(tache['date_limite'], quote=True)}' required>
    <p><button type='submit'>Enregistrer</button> <a href='/'>Annuler</a></p></form></section>"""
    return html_page(contenu, 'Modifier une tâche')


class GestionnaireHTTP(BaseHTTPRequestHandler):
    def repondre(self, contenu, status=200, localisation=None):
        self.send_response(status)
        if localisation:
            self.send_header('Location', localisation)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.send_header('Cache-Control', 'no-store')
        self.end_headers()
        self.wfile.write(contenu.encode('utf-8'))

    def do_GET(self):
        route = urlsplit(self.path)
        param = parse_qs(route.query)
        try:
            if route.path == '/':
                self.repondre(afficher_accueil(param.get('cours', [''])[0], param.get('statut', ['toutes'])[0], param.get('message', [''])[0]))
            elif route.path == '/modifier':
                self.repondre(afficher_modification(gestion.obtenir(param.get('id', [''])[0])))
            else:
                self.repondre(html_page('<section>Page introuvable. <a href="/">Accueil</a></section>'), 404)
        except (ErreurValidation, ErreurDonnees) as erreur:
            self.repondre(html_page('<section class="message">'+escape(str(erreur))+' <a href="/">Retour</a></section>'), 400)

    def do_POST(self):
        route = urlsplit(self.path).path
        try:
            longueur = int(self.headers.get('Content-Length', '0'))
            if not 0 <= longueur <= 20_000:
                raise ErreurValidation('Taille des données dépassée.')
            donnees = parse_qs(self.rfile.read(longueur).decode('utf-8'), keep_blank_values=True)
            champ = lambda nom: donnees.get(nom, [''])[0]
            if route == '/ajouter':
                gestion.ajouter(champ('titre'), champ('cours'), champ('date_limite'))
                message = 'Tâche ajoutée avec succès.'
            elif route == '/modifier':
                gestion.modifier(champ('id'), champ('titre'), champ('cours'), champ('date_limite'))
                message = 'Tâche modifiée.'
            elif route == '/terminer':
                gestion.basculer_terminee(champ('id'))
                message = 'Statut du travail modifié.'
            elif route == '/supprimer':
                gestion.supprimer(champ('id'))
                message = 'Tâche supprimée.'
            else:
                self.repondre(html_page('Action inconnue.'), 404)
                return
            self.repondre('', status=303, localisation='/?message=' + quote(message))
        except (UnicodeError, ValueError, ErreurDonnees) as erreur:
            self.repondre(html_page('<section class="message">'+escape(str(erreur))+' <a href="/">Retour</a></section>'), 400)


if __name__ == '__main__':
    print('Le programme est accessible sur http://127.0.0.1:' + os.environ.get('OMNIVOX_PORT', '8000'))
    port = int(os.environ.get('OMNIVOX_PORT', '8000'))
    HTTPServer(('127.0.0.1', port), GestionnaireHTTP).serve_forever()
