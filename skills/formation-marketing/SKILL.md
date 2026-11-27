---
name: formation-marketing
description: Votre directeur marketing pour une formation. Transforme le panel d'acheteurs et la carte des concurrents en un positionnement, un titre et une promesse, les canaux qu'utilisent vraiment les acheteurs visés (LinkedIn, réseau, prescripteurs, catalogues d'organismes, plateformes, courriel, bouche-à-oreille), une campagne de 30 jours datée pour remplir la première session, dix accroches, un budget et les chiffres à suivre. Chaque message répond à une objection réelle ou simulée. À utiliser quand l'utilisateur dit « comment vendre ma formation », « comment remplir ma session », « plan marketing », « trouver des participants », « où communiquer », « écris mes posts », « positionnement », ou « quel titre ».
argument-hint: "[budget]"
---

# formation-marketing

> Dans Formateur 360, chaque formation a son dossier `cours/<cours>/` ; l'étape vente écrit dans `cours/<cours>/vente/`. Remplacez `<cours>` par le nom court du cours (demandez-le s'il n'est pas clair, ou reprenez celui du dossier existant). Si `cours/<cours>/00-brief.md` existe, lisez-le : il contient public, durée, niveau et modalité.

Une formation dont personne n'entend parler n'existe pas. Ce skill prévoit comment
les premiers acheteurs en entendent parler, à partir de ce que le reste du pack a
appris plutôt que d'une recette générique.

## Étape 1 : lire les preuves

- `cours/<cours>/vente/panel/resultats.md` : qui achète, qui n'achète pas, et pourquoi. Le type
  d'acheteur et les segments au meilleur taux d'achat forment le premier public. Les
  principales objections sont ce à quoi le marketing doit répondre.
- `cours/<cours>/vente/concurrents.md` : comment les concurrents se présentent (pour ne pas leur
  ressembler) et le créneau.
- `cours/<cours>/vente/offre.md` et `cours/<cours>/vente/prix.md` : ce qui est vendu, à quel prix.
- `cours/<cours>/vente/chiffres.json` et `cours/<cours>/vente/cfo.md` : ce que rapporte un participant
  ou une session, ce qui plafonne ce qu'on peut dépenser pour en gagner un.

Si rien de cela n'existe, dites ce qui manque et proposez `/formation-panel --quick`
d'abord. N'inventez pas de public.

## Étape 2 : positionnement, titre et promesse

Une phrase, puis les raisons :

```
Pour <le segment qui achète le plus>, qui <son problème avec ses mots>,
<formation> est la <catégorie> qui <le créneau>, contrairement à <l'alternative la plus proche>.
```

Donnez trois versions, recommandez-en une, et dites quelle preuve du panel la
soutient. Proposez ensuite trois titres de formation : un titre de catalogue se lit
en deux secondes et dit le résultat, pas le thème. Ce skill tient lieu de travail de
marque : nom, ton et promesse se décident ici.

## Étape 3 : les canaux

Listez où le premier public passe vraiment son attention, selon le type d'acheteur :

- entreprise ou RH : réseau direct, LinkedIn, recommandations d'anciens participants,
  prescripteurs (consultants RH, fédérations, chambres de commerce), salons, courriel
  ciblé aux responsables formation ;
- particulier : LinkedIn, groupes professionnels, plateformes de formation en ligne,
  contenu gratuit (webinaire, article, vidéo), bouche-à-oreille ;
- organisme public : appels à projets, référencements et catalogues officiels,
  rencontres avec les conseillers ;
- organisme de formation : prise de contact directe avec les responsables de
  catalogue, sous-traitance d'une première session.

Pour chaque canal : pourquoi il convient à cet acheteur, coût approximatif (en argent
et en jours), et comment savoir s'il a marché. Choisissez-en deux ou trois pour
commencer ; dites ce que vous ne faites pas et pourquoi.

## Étape 4 : la campagne de 30 jours

`cours/<cours>/vente/marketing.md` reçoit un calendrier daté de J-30 à la première session :
ce qui part chaque jour, sur quel canal, avec quel message. Incluez :

- **Dix accroches**, chacune répondant à une objection du panel ou reprenant une
  raison d'achat, écrites pour leur format (première ligne d'un post, objet de
  courriel, titre de page).
- Un contenu gratuit qui prouve la valeur (un outil, un extrait, une courte session
  en ligne) et invite à s'inscrire.
- L'offre de lancement de `cours/<cours>/vente/prix.md` et sa date de fin.
- Les relances : quand, à qui, avec quoi.

## Étape 5 : budget et chiffres

- La répartition du budget entre les canaux, en argent et en jours de votre temps.
- Le maximum à dépenser pour gagner un participant ou une session : à partir de ce
  que rapporte un participant (CFO) et des places déclarées par le panel, posez le calcul.
- Les trois chiffres à suivre chaque semaine (par exemple : rendez-vous obtenus,
  pré-inscriptions, taux de conversion des propositions) et le niveau qui signifie
  « il faut changer quelque chose ».

## Règles

- Pas de faux avis, faux nombre d'abonnés, faux témoignages, avant/après inventés ni
  « vu dans ».
- Les citations du panel sont des données d'étude : jamais des citations de clients
  dans une publicité.
- Signalez les partenariats rémunérés. Ne promettez ni financement, ni certification,
  ni reconnaissance que la formation n'a pas. Ce n'est pas un conseil juridique.

## Sortie

`cours/<cours>/vente/marketing.md`. Suite : `/formation-logistique`, puis `/formation-lancement`.
