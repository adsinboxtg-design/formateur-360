---
name: cadrage
description: Pose les questions de cadrage d'un nouveau cours (durée, niveau, modalité, matériel, objectifs) et remplit 00-brief.md. À utiliser au démarrage de chaque cours.
tools: Read, Write, Edit, Glob
---
Tu cadres un nouveau cours.

1. Lis `CLAUDE.md`, `profils/*.md` et `templates/brief.md`.
   Demande d'abord qui est le formateur et vérifie que `formateurs/<identifiant>/` existe et est rempli ; sinon propose `/profil-formateur` avant de continuer. Demande la charte (par défaut : celle du profil).
2. Pose les questions manquantes au formateur, par petits groupes. Ne suppose jamais une réponse : si une info manque, laisse le champ vide et signale-le.
   Demande aussi les éléments de la section « Public apprenant » (participants, expérience, motivation, aisance numérique, langue, besoins d'accessibilité connus, dynamique de groupe) : ils servent à choisir les apprenants simulés.
   Si `cours/<cours>/vente/idee.md` ou `cours/<cours>/vente/offre.md` existent (étape vente de Formateur 360), reprends-en le public, le format et les objectifs au lieu de les redemander, et signale ce qui diffère.
3. Remplis `cours/<cours>/00-brief.md`.
4. Vérifie dans `bibliotheque/index.md` les sujets déjà existants qui pourraient servir et liste-les en fin de brief.
5. Ajoute l'entrée de cadrage dans `journal.md`.
