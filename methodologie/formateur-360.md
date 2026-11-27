# Formateur 360 : le parcours complet

> Fichier rédigé le 24/11/2026 à partir des skills du pack. `/formateur-360` le lit pour dire où en est un cours et proposer l'étape suivante.

Chaque formation a son dossier `cours/<cours>/`. Le parcours a trois temps : **vendre**, **concevoir**, **faire valider**. Avant le premier cours : `/init-espace`, puis `/premiere-utilisation` (outils, connecteurs, profil formateur, charte).

## 1. Vendre : la formation se vendra-t-elle et rapportera-t-elle ?

Fichiers dans `cours/<cours>/vente/`, dans cet ordre :

| Étape | Commande | Ce qu'elle produit |
|---|---|---|
| 1 | `/formation-conseil` | Un conseil de trois lentilles (Offres, Monopole, Transfert) note le projet et vote : financer, financer si, passer. |
| 2 | `/formation-concurrents` | Concurrents directs, indirects et substituts, à partir de sources publiques liées ; créneau libre. |
| 3 | `/formation-panel` | Panel d'acheteurs simulés (100, ou 20 avec `--quick`) : taux d'achat, refus, réponses de prix. |
| 4 | `/formation-prix` | Fourchette de prix (Van Westendorp), confrontée aux concurrents et au taux journalier visé. |
| 5 | `/formation-offre` | Offre complète : obstacles levés, bonus, garantie, urgence réelle, nom. |
| 6 | `/formation-cfo` | Seuil de rentabilité, gain réel par jour mobilisé, résultat de l'année 1, scénarios dégradés. |
| 7 | `/formation-marketing` | Positionnement, titre, canaux, campagne de 30 jours, accroches, budget. |
| 8 | `/formation-logistique` | Lieux ou outils, matériel, inscriptions, facturation, obligations et agréments à vérifier, risques. |
| 9 | `/formation-lancement` | Test réel peu coûteux, compte à rebours jusqu'à la première session, jour J, 30 jours après. |
| 10 | `/formation-dossier` | Dossier de lancement unique, avec un verdict calculé : Rentable, Pas encore ou Incomplet. |

Règles :
- Pas de conception lourde avant un minimum de preuve de vente : commencer par `/formation-conseil` et `/formation-cfo`, les moins coûteux.
- Formation imposée ou commande ferme : le formateur peut passer directement à la conception ; le noter dans `journal.md`.
- Verdict « Pas encore » : traiter d'abord le premier contrôle en échec.

## 2. Concevoir : le cours lui-même

`/nouveau-cours` crée le dossier et enchaîne la chaîne de production (voir `chaine-de-production.md`) :

| Fichier | Contenu | Agent ou skill |
|---|---|---|
| `00-brief.md` | Durée, niveau, modalité, matériel, objectifs, public apprenant | `cadrage` |
| `01-notes/` | Notes, sources réellement consultées, vidéos | `trieur-notes`, `documentaliste`, `/recherche-sources`, `/transcription-video` |
| `02-plan.md` | Plan horodaté avec fil rouge | `planificateur` |
| `04-ateliers/` | Ateliers, fichiers de départ et corrigés | `concepteur-ateliers` |
| `03-supports/` | Diapositives, version PDF, cheatsheet | `redacteur-supports`, `/production-documents`, `/controle-visuel` |
| `05-formateur/` | Cahier du formateur | `cahier-formateur` |
| `06-evaluations/` | Évaluations et questionnaire de retour | `evaluations`, `/export-google-forms` |

## 3. Faire valider : apprenants simulés puis jury

| Étape | Commande | Ce qu'elle produit |
|---|---|---|
| Plan et ateliers | `/simulation-cours` | Avocat du diable et 3 à 5 apprenants choisis selon `profils/apprenants.md` ; `simulations/<cible>-synthese.md` |
| Supports | `/validation-supports` | 3 à 5 apprenants sur les supports ; `simulations/supports-synthese.md` |
| Jury | `/jury-experts` (ou `--rapide`) | Cinq membres sur la grille de `profils/jury.md` ; `jury/notes.md` (décision calculée), `jury/deliberation.md` |
| Relecture finale | agent `relecteur` | `07-relecture.md` : sources, `[À VÉRIFIER]` restants, voix, charte, timing |

Ordre : simulations, puis validation des supports, puis jury, puis relecture finale. Le formateur décide de chaque correction (retenue ou rejetée) ; les décisions vont dans `journal.md` avant toute modification.

## Coûts

Un panel de 100 acheteurs, une validation à 5 apprenants ou un jury complet lancent de nombreux sous-agents. Proposer la version rapide quand elle existe (`--quick`, `--rapide`) et annoncer le coût avant de lancer.

## Après la première session

Reporter les retours réels dans `journal.md`, comparer avec les constats simulés, et relancer seulement les étapes concernées.
