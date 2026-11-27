---
name: formation-conseil
description: 'Votre conseil d''administration pour une formation. Soumet un projet de formation à un conseil de trois membres, chacun un sous-agent qui lit le projet à travers un cadre publié : la lentille Offres (d''après $100M Offers d''Alex Hormozi), la lentille Monopole (d''après Zero to One de Peter Thiel) et la lentille Transfert (d''après le modèle d''évaluation de Kirkpatrick). Chacun note le projet, nomme les risques qui le tueraient et vote : financer, financer si, ou passer. À utiliser quand l''utilisateur dit « teste mon idée de formation », « est-ce que cette formation va marcher », « challenge ma formation », « qu''en dirait un conseil », ou démarre le pack formateur sur une nouvelle formation.'
argument-hint: "<le projet de formation, ou vide pour reprendre la conversation>"
---

# formation-conseil

> Dans Formateur 360, chaque formation a son dossier `cours/<cours>/` ; l'étape vente écrit dans `cours/<cours>/vente/`. Remplacez `<cours>` par le nom court du cours (demandez-le s'il n'est pas clair, ou reprenez celui du dossier existant). Si `cours/<cours>/00-brief.md` existe, lisez-le : il contient public, durée, niveau et modalité.

La première réunion. Avant de concevoir les supports ou de réserver une salle,
trois membres du conseil démontent le projet, chacun sous un angle différent, et
votent.

Ce que l'utilisateur a tapé après `/formation-conseil` : `$ARGUMENTS`. Si c'est
vide, prenez le projet dans la conversation.

## La règle sur les trois noms

Les lentilles résument des **cadres publiés**, rien de plus. Les membres du conseil
ne sont pas ces personnes, ne parlent jamais en leur nom, ne les citent jamais, ne
prétendent jamais qu'elles approuveraient quoi que ce soit. Écrivez « la lentille
Offres », jamais « Alex Hormozi dit ». Si l'utilisateur demande ce que l'une d'elles
penserait vraiment, répondez que vous pouvez seulement appliquer son cadre public.

## Étape 0 : le fichier de l'idée

Tout le pack lit `cours/<cours>/vente/idee.md` dans le projet de l'utilisateur. S'il n'existe
pas, écrivez-le maintenant à partir de la conversation :

```markdown
# <titre de la formation, ou titre provisoire>

- Ce que c'est : une phrase.
- Pour qui : le public participant, aussi précis que possible.
- Qui achète : entreprise ou RH, particulier, organisme public, organisme de formation (un ou plusieurs).
- Le résultat promis : ce que les participants sauront faire, et ce que ça change pour l'acheteur.
- Format et prix : durée, présentiel, distanciel ou mixte, taille de groupe, prix par participant ou par session.
- Où et comment : pays ou région, comment les acheteurs la trouvent.
- Le formateur : expérience utile sur ce sujet, preuves existantes (références, évaluations).
- Contraintes : budget, temps disponible, ce qui est déjà décidé ou déjà conçu.
```

S'il manque le titre, le public, l'acheteur, le format ou le prix, demandez-les (trois
questions au plus, en un seul message), puis écrivez le fichier. N'inventez ni
budget, ni taille de marché, ni concurrent, ni référence client.

Si `cours/<cours>/00-brief.md` existe déjà pour ce cours, lisez-le : il contient la durée, le niveau, la modalité et les objectifs.

## Étape 1 : préparer le dossier du conseil

Écrivez `cours/<cours>/vente/conseil/dossier.md` : le fichier de l'idée plus tout ce que
l'utilisateur a dit qu'un inconnu devrait savoir. **Les sous-agents ne voient pas
cette conversation** : le dossier doit se suffire à lui-même. N'y ajoutez pas votre
propre avis sur le projet.

## Étape 2 : réunir le conseil

Lancez trois sous-agents dans UN SEUL message (outil Agent, `subagent_type:
general-purpose`, un par membre), avec chacun cette consigne : `Lis
cours/<cours>/vente/conseil/dossier.md et le fichier lentilles.md (chemin ci-dessous),
applique UNIQUEMENT la lentille <nom>, et écris ton mémo dans
cours/<cours>/vente/conseil/<nom>.md, en français.` Le fichier des lentilles est
`lentilles.md` dans le dossier de ce skill (`${CLAUDE_SKILL_DIR}/lentilles.md` ; si
ce chemin n'est pas développé, utilisez le dossier de base que Claude Code a affiché
pour ce skill). Les noms : `offres`, `monopole`, `transfert`.

Chaque mémo suit cette forme :

```markdown
# Lentille <Nom>
Note : <1-10> | Vote : FINANCER / FINANCER SI / PASSER
## Ce qui est solide
## Ce qui la tuerait (les 3 premiers, le plus dangereux d'abord)
## Les questions que je poserais au formateur
## Si FINANCER SI : les conditions
```

## Étape 3 : la synthèse du président

Lisez les trois mémos (ils sont courts) et écrivez `cours/<cours>/vente/conseil.md` :

1. Le vote, par exemple « 2 financer si, 1 passer », et la note moyenne.
2. Les risques soulevés par plusieurs membres : ils passent en premier.
3. Toutes les conditions, fusionnées en une liste à cocher que le reste du pack
   pourra vérifier (le panel, le prix et le CFO en testeront la plupart).
4. Un paragraphe : la version la plus forte de cette formation que le conseil
   voit. Elle peut différer de ce que l'utilisateur a présenté ; dites-le clairement.

Gardez les désaccords entre membres. Un conseil d'accord sur tout n'a pas fait son
travail.

## Règles

- Notez la formation, pas le formateur.
- Aucun fait inventé. Si une lentille a besoin d'un chiffre que personne n'a encore
  (taille du marché, coût d'acquisition d'un client, taux de remplissage), nommez-le
  comme question ouverte et dites quel skill y répond (`/formation-concurrents`,
  `/formation-panel`, `/formation-cfo`).
- PASSER est un résultat, pas un échec. Dites-le simplement.
- En français, sans tiret cadratin.

## Sortie

`cours/<cours>/vente/idee.md`, `cours/<cours>/vente/conseil/` (dossier et trois mémos),
`cours/<cours>/vente/conseil.md`. Donnez ensuite le vote en une ligne et proposez la suite :
`/formation-concurrents` pour voir qui est déjà là, ou `/formation-panel` pour
présenter l'offre à 100 acheteurs simulés.

## La suite du pack

```
conseil -> concurrents -> panel -> prix -> offre -> cfo -> marketing -> logistique -> lancement -> dossier
```

Chaque skill peut aussi tourner seul ; chacun lit ce qui existe déjà dans `cours/<cours>/vente/`.
Une fois le verdict « Rentable » obtenu, la conception du cours lui-même se fait avec
`/nouveau-cours`, la partie conception de Formateur 360.
