---
name: formateur-360
description: Point d'entrée de Formateur 360. Guide le formateur de l'idée de formation à la première session en trois temps (vendre, concevoir, faire valider), dit où en est un cours en lisant son dossier, et propose l'étape suivante avec la bonne commande. À utiliser quand l'utilisateur dit « formateur 360 », « par où je commence », « où en est ma formation », « quelle est la prochaine étape », « nouvelle formation », ou ne sait pas quelle commande lancer.
argument-hint: "[nom du cours]"
---

# formateur-360

Le chef d'orchestre. Il ne produit rien lui-même : il regarde où en est un cours et oriente vers la bonne commande. Lisez `methodologie/formateur-360.md` pour le parcours complet.

## Étape 1 : quel cours

Ce que l'utilisateur a tapé après `/formateur-360` : `$ARGUMENTS`. Listez les dossiers de `cours/`. Si le cours n'existe pas, demandez son nom court et proposez de commencer. Si `formateurs/` n'a aucun profil rempli, proposez d'abord `/premiere-utilisation` ou `/profil-formateur`.

## Étape 2 : l'état du cours

Regardez quels fichiers existent dans `cours/<cours>/` et donnez l'état en trois lignes :

| temps | fichiers qui prouvent l'étape | commande |
|---|---|---|
| **1. Vendre** : la formation se vendra-t-elle et rapportera-t-elle ? | `vente/conseil.md`, `vente/concurrents.md`, `vente/panel/resultats.md`, `vente/prix.md`, `vente/offre.md`, `vente/cfo.md`, `vente/marketing.md`, `vente/logistique.md`, `vente/lancement.md`, `vente/dossier.md` | `/formation-conseil` ... `/formation-dossier` |
| **2. Concevoir** : le cours lui-même | `00-brief.md`, `01-notes/`, `02-plan.md`, `03-supports/`, `04-ateliers/`, `05-formateur/`, `06-evaluations/` | `/nouveau-cours` (enchaîne la chaîne de production) |
| **3. Faire valider** : apprenants simulés puis jury d'experts | `simulations/*-synthese.md`, `jury/deliberation.md`, `07-relecture.md` | `/simulation-cours`, `/validation-supports`, `/jury-experts` |

Si `vente/dossier.md` existe, citez son verdict tel qu'il est écrit (ligne « Verdict »). Ne recalculez rien et ne déduisez pas un verdict absent.

## Étape 3 : l'étape suivante

Proposez UNE étape suivante, avec sa commande et ce qu'elle produira. Règles :

- Pas de conception lourde avant un minimum de preuve de vente : si rien n'existe dans `vente/`, proposez `/formation-conseil` puis `/formation-cfo` (les deux moins coûteux) avant `/nouveau-cours`. Si le formateur veut concevoir quand même (commande ferme, formation imposée), respectez son choix et notez-le dans `journal.md`.
- Si le verdict est « Pas encore », proposez le skill qui traite le premier contrôle en échec.
- Après la validation des supports, proposez `/jury-experts` avant la relecture finale.
- Signalez les coûts : un panel de 100 acheteurs ou un jury complet lance de nombreux sous-agents ; proposez la version rapide quand elle existe.

## Sortie

Aucun fichier. L'état du cours en trois lignes et une seule étape suivante.
