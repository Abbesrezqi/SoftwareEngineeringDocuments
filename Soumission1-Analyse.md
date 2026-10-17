# Omnivox — Réservation de salles d’étude

## Soumission 1 — Cahier des charges initial

**Cours :** Analyse et modélisation de système d’information  
**Code :** 420-AS2-AS  
**Session :** Automne 2026  
**Membres :** Abbes Rezqi et Ali Rechachi

---

## 1. Présentation du projet

Notre projet propose un module de réservation de salles d’étude dans Omnivox. Il permettra aux étudiants de consulter les disponibilités et de réserver une salle. Le responsable pourra gérer les salles, les horaires et les réservations.

Ce document présente le besoin, la portée, les exigences et le backlog initial.

Le contexte retenu est celui d’un collège fictif où les demandes passent par un responsable et sont inscrites dans un calendrier partagé. Cette organisation peut entraîner des délais de réponse et des conflits d’horaire. Il s’agit d’une hypothèse de travail à valider, et non d’une description du fonctionnement réel d’Omnivox.

### Objectif

Centraliser les réservations, rendre les disponibilités visibles et empêcher deux réservations actives pour une même salle au même moment.

Le projet porte sur l’analyse et la conception du module. Aucune application fonctionnelle ne sera livrée.

---

## 2. Parties prenantes et besoins

| Partie prenante | Besoins |
| --- | --- |
| Étudiants | Trouver une salle adaptée à leur groupe, réserver un créneau et consulter ou annuler leurs réservations. |
| Responsable des salles | Définir les disponibilités, bloquer une salle et consulter les réservations pour organiser son utilisation. |
| Administrateur informatique | Contrôler les droits d’accès et prévoir la connexion avec les comptes du collège. |
| Direction du collège | Disposer de règles communes de réservation et limiter les conflits d’utilisation. |

---

## 3. Portée et règles proposées

### Éléments inclus

Le module comprend :

- La consultation des salles et de leurs disponibilités.
- La réservation d’une salle.
- L’annulation d’une réservation.
- La confirmation à l’écran.
- La consultation des réservations personnelles.
- La gestion des salles et des horaires.

Il couvre **un seul campus** et uniquement les **salles d’étude**.

### Éléments hors portée

Les éléments suivants sont exclus :

- La gestion des notes et des cours.
- Les frais scolaires et les paiements.
- La messagerie MIO.
- Les réservations de matériel.
- Les réservations récurrentes.
- Les listes d’attente.
- Les notifications par courriel ou SMS.

Le projet ne prévoit pas de modifier le véritable système Omnivox.

### Règles métier à valider avec le collège

1. Les créneaux durent **30 minutes**. Une réservation dure de **30 minutes à 2 heures** et se fait au plus **14 jours à l’avance**.
2. Un étudiant peut avoir au maximum **deux réservations futures actives** et ne peut pas réserver deux salles sur des horaires qui se chevauchent.
3. Le nombre de participants doit être au moins égal à **1** et ne peut pas dépasser la capacité de la salle.
4. Une réservation doit être entièrement comprise dans une plage ouverte, sans chevauchement avec une réservation active ou un blocage. Deux réservations consécutives sont permises.
5. L’étudiant peut annuler sa réservation avant son heure de début. Le responsable peut annuler une réservation future en indiquant un motif.
6. Une réservation annulée reste dans l’historique et libère immédiatement le créneau.
7. Le blocage d’une salle est refusé si des réservations actives se trouvent sur la période. Le responsable doit d’abord les annuler.

---

## 4. Exigences fonctionnelles

| Identifiant | Exigence |
| --- | --- |
| **EF01** | Reconnaître le compte connecté et appliquer les droits correspondant au rôle étudiant, responsable ou administrateur. |
| **EF02** | Afficher les salles actives avec leur nom, leur localisation, leur capacité et leurs équipements. |
| **EF03** | Afficher les créneaux disponibles pour une date et un nombre de participants, en excluant les fermetures, les blocages et les réservations actives. |
| **EF04** | Créer une réservation en vérifiant toutes les règles métier et refuser toute demande invalide avec une explication. |
| **EF05** | Afficher après validation un numéro de réservation unique, la salle, la date, les heures et le statut confirmé. |
| **EF06** | Permettre à l’étudiant de consulter uniquement ses propres réservations, avec leur statut confirmé ou annulé. |
| **EF07** | Permettre à l’étudiant d’annuler une réservation future lui appartenant et rendre le créneau disponible. |
| **EF08** | Permettre au responsable d’ajouter et de modifier une salle, ses équipements et ses horaires. Refuser sa désactivation si elle possède des réservations futures actives. |
| **EF09** | Permettre au responsable de bloquer une période et d’annuler une réservation future avec un motif visible par l’étudiant concerné. |
| **EF10** | Permettre au responsable de consulter les réservations par salle et par date. |
| **EF11** | Permettre à l’administrateur d’attribuer ou de retirer le rôle de responsable. Refuser cette action aux autres rôles. |

---

## 5. Exigences non fonctionnelles

Ces exigences représentent des cibles pour le futur système. Elles seront précisées dans les modèles et les scénarios de validation.

### ENF01 — Sécurité

Toute tentative d’accès à une réservation d’un autre étudiant ou à une fonction non autorisée doit être refusée, même par accès direct.

### ENF02 — Performance

Pour **50 utilisateurs simultanés** et **20 salles**, **95 % des recherches de disponibilités** doivent répondre en moins de **2 secondes** dans l’environnement de test prévu.

### ENF03 — Facilité d’utilisation

Après connexion, un étudiant doit pouvoir réserver une salle disponible en **trois écrans au maximum**, confirmation comprise.

### ENF04 — Compatibilité

Les parcours de consultation, de réservation et d’annulation doivent fonctionner sans défilement horizontal sur des largeurs de **390 à 1440 pixels**, avec **Chrome** et **Edge**.

### ENF05 — Fiabilité

Si deux étudiants demandent simultanément le même créneau, une seule réservation doit être confirmée. L’autre demande doit recevoir un message d’indisponibilité.

---

## 6. Contraintes, hypothèses et faisabilité

### Contraintes

- Le travail doit être réalisé par une équipe de **2 à 4 étudiants** pendant la session, selon les échéances publiées dans Léa.
- Les livrables sont des documents et des modèles. Les exemples utiliseront des comptes, des salles et des réservations fictifs.
- Aucun accès au code, aux données ou aux interfaces internes du véritable Omnivox n’est prévu.
- La documentation sera conservée dans une copie du dépôt fourni par le professeur.
- Le suivi des tâches sera organisé dans **GitHub Projects**.

### Hypothèses

- Le collège fournirait des comptes authentifiés et les rôles nécessaires au module. La connexion réelle reste à étudier avant toute réalisation.
- Le responsable disposerait d’une liste des salles, de leurs capacités et de leurs horaires.
- Les utilisateurs auraient une connexion Internet et un navigateur compatible.
- Les règles proposées seraient validées par le collège avant le développement.

### Faisabilité technique

Les fonctions reposent sur des données simples : utilisateurs, salles, horaires et réservations.

La principale difficulté est de garantir qu’un créneau ne soit pas réservé deux fois. Une intégration réelle à Omnivox dépendrait toutefois de l’autorisation du fournisseur et des possibilités techniques disponibles.

### Faisabilité organisationnelle

Un responsable doit tenir les horaires à jour et traiter les fermetures exceptionnelles.

Le principal risque est une différence entre les disponibilités affichées et l’utilisation réelle des salles. Des règles communes et une mise à jour régulière réduiront ce risque.

### Faisabilité pour le projet scolaire

GitHub et un outil de diagrammes suffisent pour le travail scolaire. Aucun achat n’est prévu.

La portée limitée à un campus permet de réaliser l’analyse pendant la session. Le coût d’un déploiement réel n’est pas estimé à cette étape.

---

## 7. Organisation du Product Backlog

Le backlog comporte **trois Epics** et **huit User Stories**.

- **P1 :** fonctions essentielles à analyser en premier.
- **P2 :** fonctions de gestion à préciser ensuite.
- **Statut initial :** toutes les stories sont « À faire ».

| Epic | Description | User Stories |
| --- | --- | --- |
| **E1** | Consulter les salles | US01 et US02 |
| **E2** | Gérer ses réservations | US03, US04 et US05 |
| **E3** | Administrer les salles et les accès | US06, US07 et US08 |

### Ordre proposé

**US01 → US02 → US03 → US04 → US05 → US06 → US07 → US08**

Les droits et les données de base seront définis dès le début pour rendre les scénarios cohérents.

---

## 8. User Stories et critères d’acceptation

### US01 — Consulter les salles

**Epic :** E1  
**Priorité :** P1  
**Exigences liées :** EF01 et EF02

En tant qu’étudiant, je veux consulter les salles et leurs caractéristiques afin de choisir une salle adaptée à mon groupe.

**Critères d’acceptation :**

- Un étudiant connecté voit uniquement les salles actives avec leur localisation, leur capacité et leurs équipements.
- Une personne non connectée ne peut pas accéder au module.

### US02 — Rechercher un créneau

**Epic :** E1  
**Priorité :** P1  
**Exigence liée :** EF03

En tant qu’étudiant, je veux rechercher une disponibilité par date et par nombre de participants afin de trouver un créneau adapté.

**Critères d’acceptation :**

- Pour une date autorisée et un nombre positif de participants, seules les salles de capacité suffisante et leurs plages libres sont proposées.
- Un créneau réservé ou bloqué n’est pas proposé.
- Si aucun résultat ne correspond, un message le précise.

### US03 — Réserver une salle

**Epic :** E2  
**Priorité :** P1  
**Exigences liées :** EF04 et EF05

En tant qu’étudiant, je veux réserver un créneau disponible afin de disposer d’une salle pour étudier.

**Critères d’acceptation :**

- Une demande conforme reçoit un numéro unique et une confirmation avec la salle, la date et les heures.
- Une durée supérieure à 2 heures, un chevauchement ou une troisième réservation future active entraîne un refus expliqué.
- Si deux demandes simultanées concernent le même créneau, une seule est confirmée.

### US04 — Consulter mes réservations

**Epic :** E2  
**Priorité :** P1  
**Exigence liée :** EF06

En tant qu’étudiant, je veux consulter mes réservations afin de retrouver les informations de mes séances de travail.

**Critères d’acceptation :**

- La liste affiche uniquement les réservations du compte connecté, leur salle, leurs horaires et leur statut.
- Un accès direct à la réservation d’un autre étudiant est refusé.

### US05 — Annuler ma réservation

**Epic :** E2  
**Priorité :** P1  
**Exigence liée :** EF07

En tant qu’étudiant, je veux annuler une réservation future afin de libérer la salle lorsque je n’en ai plus besoin.

**Critères d’acceptation :**

- L’annulation d’une réservation future appartenant au compte connecté change son statut et libère le créneau.
- L’annulation d’une réservation déjà commencée ou appartenant à un autre étudiant est refusée.

### US06 — Gérer les salles

**Epic :** E3  
**Priorité :** P2  
**Exigence liée :** EF08

En tant que responsable, je veux gérer les salles et leurs horaires afin de publier des informations exactes.

**Critères d’acceptation :**

- Une salle doit avoir un nom, une localisation et une capacité entière supérieure à zéro.
- La désactivation d’une salle ayant des réservations futures actives est refusée.

### US07 — Gérer les indisponibilités

**Epic :** E3  
**Priorité :** P2  
**Exigences liées :** EF09 et EF10

En tant que responsable, je veux consulter les réservations et gérer les fermetures afin de tenir compte des besoins du collège.

**Critères d’acceptation :**

- Le filtre par salle et date ne retourne que les réservations correspondantes.
- Une annulation par le responsable exige un motif et libère le créneau.
- Le motif est visible dans la réservation de l’étudiant.
- Un blocage est refusé tant qu’une réservation active chevauche la période.

### US08 — Gérer les droits

**Epic :** E3  
**Priorité :** P2  
**Exigences liées :** EF01 et EF11

En tant qu’administrateur, je veux attribuer le rôle de responsable afin de réserver les fonctions de gestion aux personnes autorisées.

**Critères d’acceptation :**

- L’administrateur peut attribuer et retirer le rôle de responsable à un compte existant.
- Un étudiant ou un responsable ne peut pas modifier les rôles.

Les critères ci-dessus serviront à vérifier les scénarios et les modèles. Les tests du logiciel ne sont pas à réaliser dans ce projet d’analyse.

---

## 9. Definition of Done de l’équipe

Une tâche d’analyse ou de modélisation est considérée comme terminée lorsque les conditions suivantes sont respectées :

- Le contenu prévu est rédigé et répond au besoin de la tâche.
- Les exigences concernées et les critères d’acceptation sont couverts par le document ou le scénario produit.
- Les termes et les règles sont cohérents avec le cahier des charges et le backlog.
- Un autre membre a relu le travail et les corrections nécessaires ont été intégrées.
- Le document est lisible, sans section obligatoire vide, et les exemples utilisent uniquement des données fictives.
- La version à jour est déposée sur GitHub et le lien fonctionne pour le professeur.
- La tâche est déplacée dans « Terminé » dans le tableau de suivi après la revue.

---

## 10. Travail prévu pour la soumission 2

Nous mettrons à jour les exigences, la portée et le backlog à partir de la rétroaction reçue.

Nous réaliserons le **diagramme de cas d’utilisation** et détaillerons quatre scénarios :

1. Rechercher un créneau.
2. Réserver une salle.
3. Annuler une réservation.
4. Bloquer une période.

Nous représenterons ensuite le processus actuel retenu comme hypothèse et le processus proposé avec **deux diagrammes d’activités**.

Le **modèle de données** précisera les utilisateurs, les salles, les disponibilités et les réservations, ainsi que leurs relations.

Une courte justification de la **normalisation** et un **rapport de progression de 3 à 5 pages** accompagneront cette remise.

---

## 11. Dépôt GitHub

La documentation du projet est accessible dans notre dépôt :

[Consulter le dépôt du projet Omnivox](https://github.com/Abbesrezqi/SoftwareEngineeringDocuments)
