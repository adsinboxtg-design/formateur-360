---
name: formation-offre
description: Construit une offre de formation difficile à refuser. Liste tous les obstacles que l'acheteur et le participant rencontrent avant, pendant et après la formation, transforme chacun en solution, garde ce qui coûte peu à livrer et vaut beaucoup, et empile le tout avec des bonus honnêtes (suivi à 30 jours, outils, diagnostic préalable), une garantie que le CFO peut assumer, une urgence réelle et un nom clair. Note l'offre sur l'équation de valeur et la reteste sur un panel rapide. À utiliser quand l'utilisateur dit « améliore mon offre », « pourquoi personne ne s'inscrit », « qu'est-ce que j'inclus », « garantie », « bonus », « rendre ma formation irrésistible », ou après un panel où beaucoup refusent.
argument-hint: "[la formation]"
---

# formation-offre

> Dans Formateur 360, chaque formation a son dossier `cours/<cours>/` ; l'étape vente écrit dans `cours/<cours>/vente/`. Remplacez `<cours>` par le nom court du cours (demandez-le s'il n'est pas clair, ou reprenez celui du dossier existant). Si `cours/<cours>/00-brief.md` existe, lisez-le : il contient public, durée, niveau et modalité.

La plupart des formateurs vendent un programme. Les bons vendent une offre : la
formation plus tout ce qui fait de l'achat un oui facile, pour celui qui paie comme
pour celui qui participe. Ce skill la construit, avec la lentille Offres de
`../formation-conseil/lentilles.md` comme méthode (un résumé du cadre de *$100M
Offers* d'Alex Hormozi ; ne le présentez jamais comme ses mots) et la lentille
Transfert pour ce qui se passe après la formation.

## Étape 1 : lire ce qui est déjà connu

- `cours/<cours>/vente/idee.md` et `cours/<cours>/vente/offre-panel.md` : ce qui est proposé aujourd'hui.
- `cours/<cours>/vente/panel/resultats.md` : pourquoi les acheteurs refusent, avec leurs mots.
  C'est la matière première : chaque objection principale doit trouver une réponse
  dans l'offre.
- `cours/<cours>/vente/concurrents.md` : les plaintes sur les formations concurrentes.
- `cours/<cours>/vente/chiffres.json` : ce que coûte chaque ajout, pour que l'empilement reste
  rentable par jour mobilisé.
- `cours/<cours>/vente/conseil.md` : les conditions du conseil.

## Étape 2 : la liste des obstacles

Écrivez chaque obstacle entre l'acheteur et le résultat qu'il veut, avec ses mots, en
séparant celui qui paie et celui qui participe quand ce ne sont pas les mêmes :

- avant d'acheter : doute sur le résultat, prix, justification en interne, temps
  hors du poste, financement, choix de la date ;
- pendant : niveau inadapté, cas trop théoriques, groupe hétérogène ;
- après : rien ne change au poste, pas de suivi, oubli, manager qui ne soutient pas.

Visez 15 à 30 obstacles. Partez des objections du panel et des plaintes sur les
concurrents.

## Étape 3 : solutions, triées et empilées

Transformez chaque obstacle en solution (un diagnostic préalable, des exercices sur
les cas des participants, un outil utilisable dès le lendemain, un rappel ou une
séance de suivi à 30 jours, un point avec le manager, une attestation, un format
plus court, une version intra). Notez chacune sur la valeur pour l'acheteur (1 à 5)
et le coût de livraison (1 à 5, en jours de votre temps et en argent, d'après les
chiffres du CFO). Gardez ce qui vaut beaucoup et coûte peu. Empilez ce qui reste :

- **Le cœur** : la formation elle-même, décrite par le résultat, pas par le
  programme.
- **Les bonus** : deux ou trois, chacun neutralisant une objection précise.
- **La garantie** : ce qui se passe si la formation ne tient pas sa promesse (une
  session de rattrapage, un accompagnement offert, un remboursement partiel).
  Chiffrez son coût à un taux de réclamation réaliste avec l'outil du CFO avant de la
  promettre.
- **Urgence et rareté** : seulement si elles sont vraies (places limitées par la
  taille réelle du groupe, prix de la session pilote jusqu'à une date). Jamais de
  faux compte à rebours.
- **Le nom** : un nom d'offre clair et précis.

## Étape 4 : la noter

Sur l'équation de valeur, avant et après, de 1 à 10 chacun : résultat rêvé,
probabilité perçue de l'obtenir, délai jusqu'au résultat, effort et sacrifice. Dites
quel élément de l'empilement fait bouger quelle note. Ajoutez, pour la lentille
Transfert : quel élément aide le comportement à changer au poste de travail.

## Étape 5 : la retester

Écrivez la nouvelle offre dans `cours/<cours>/vente/offre-panel.md` (gardez l'ancienne en
`cours/<cours>/vente/offre-panel-v1.md`) et relancez `/formation-panel --quick` avec la même
seed. Donnez le taux d'achat avant et après et les objections qui ont reculé. Si
rien n'a bougé, dites-le : le problème est peut-être le marché ou le prix, pas l'offre.

## Règles

- Chaque promesse doit être tenable et abordable ; vérifiez les coûts avec le CFO.
- Pas de faux avis, faux témoignages, fausse rareté, fausse remise, ni de « vu dans ».
- Ne promettez ni certification, ni éligibilité à un financement, ni reconnaissance
  officielle que la formation n'a pas. Suivez les règles de publicité et de protection
  du consommateur du pays de l'acheteur. Ce n'est pas un conseil juridique.

## Sortie

`cours/<cours>/vente/offre.md` (obstacles, empilement, coûts, notes, résultat du nouveau test)
et `cours/<cours>/vente/offre-panel.md` mis à jour. Suite : `/formation-cfo` pour recalculer
avec l'empilement, puis `/formation-marketing`.
