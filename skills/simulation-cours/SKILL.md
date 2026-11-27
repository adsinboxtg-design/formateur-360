---
name: simulation-cours
description: Challenge un plan ou des ateliers en lançant un avocat du diable et des apprenants simulés choisis selon le public du brief (débutant anxieux, peu numérique, pragmatique, expérimenté résistant, non natif, accessibilité, dynamique de groupe...), puis synthétise les constats pour décision du formateur.
---
# Simulation

Entrée : document cible (plan ou atelier) + cours.

1. Lire le brief (`00-brief.md`) et `profils/apprenants.md`.
2. Choisir 3 à 5 apprenants simulés selon les règles de sélection de `profils/apprenants.md`, parmi les profils marqués pour la cible (plan ou ateliers). Utiliser `apprenant-simule` pour un profil précis de niveau, modalité ou matériel. Annoncer la sélection au formateur avec une raison par profil ; il peut ajouter ou retirer un profil.
3. Lancer en parallèle, **sans leur transmettre l'historique de conception** (seulement le brief, le document cible et, pour les ateliers, leurs fichiers) :
   - `avocat-du-diable` sur le document ;
   - les apprenants retenus, en leur indiquant la cible (`plan` ou `ateliers`) pour le nom de leur fichier, et pour `apprenant-accessibilite` le besoin à vérifier.
4. Synthétiser dans `simulations/<cible>-synthese.md` : en tête, les profils lancés et pourquoi ; puis les constats dédoublonnés, triés par gravité, les points soulevés par plusieurs profils en premier.
5. Présenter la synthèse au formateur et lui demander pour chaque point bloquant/gênant : retenu ou rejeté.
6. Reporter les décisions dans `journal.md`. Ne modifier le document qu'après décision.
