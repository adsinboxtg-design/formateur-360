---
name: validation-supports
description: Valide les supports et ateliers d'un cours en les faisant passer par 3 à 5 apprenants simulés choisis selon le public du brief (expert, difficile, je-m'en-foutiste, débutant anxieux, peu numérique, pragmatique, expérimenté résistant, non natif, accessibilité), puis synthétise leurs retours pour décision du formateur.
---
# Validation des supports

Entrée : le cours (`cours/<nom>/`). Prérequis : `03-supports/` et `04-ateliers/` rédigés.

1. Lire `00-brief.md` et `profils/apprenants.md`. Choisir 3 à 5 apprenants simulés marqués pour la cible « supports », selon les règles de sélection. `apprenant-expert` est retenu dès que le sujet comporte des faits vérifiables. Annoncer la sélection au formateur avec une raison par profil ; il peut ajouter ou retirer un profil. Sans section « Public apprenant » renseignée, le dire et proposer par défaut `apprenant-expert`, `apprenant-difficile` et `apprenant-mefoutiste`.
2. Lancer **en parallèle** les profils retenus, sans leur transmettre l'historique de conception (seulement `00-brief.md`, `02-plan.md`, `03-supports/`, `04-ateliers/`, `01-notes/sources.md`), en leur indiquant la cible `supports` pour le nom de leur fichier.
3. Attendre les rapports dans `simulations/`.
4. Écrire `simulations/supports-synthese.md` :
   - en tête, les profils lancés et pourquoi ;
   - **Erreurs confirmées** (expert, avec preuve) → à corriger en priorité ;
   - **Doutes à vérifier** (expert) → passer à la skill `recherche-sources` ;
   - **Questions et objections à préparer** (difficile, expérimenté résistant) → réponses en notes orateur ou dans le cahier formateur ;
   - **Points de décrochage et de blocage** (je-m'en-foutiste, débutant anxieux, peu numérique) → reformulation, découpage, interaction, pas-à-pas ;
   - **Transfert au poste** (pragmatique) → outils, exemples, suivi à ajouter ;
   - **Langue et accessibilité** (non natif, accessibilité) → reformulations et corrections de forme, à confirmer avec des personnes concernées ;
   - points soulevés par plusieurs profils en tête de chaque rubrique.
5. Présenter la synthèse au formateur ; pour chaque point : retenu / rejeté.
6. Reporter les décisions dans `journal.md`. Ne modifier les supports qu'après décision.
7. Les réponses préparées retenues vont dans `05-formateur/cahier.md` (section « Questions probables »).
