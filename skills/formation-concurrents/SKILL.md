---
name: formation-concurrents
description: 'Cartographie toutes les formations concurrentes et le créneau qu''elles laissent libre. Trouve les concurrents directs (même sujet, même public), indirects (autre format pour le même besoin : coaching, livre, MOOC, formation interne) et les substituts (ne rien faire, apprendre sur le tas, une vidéo gratuite), à partir de sources publiques uniquement, et relève pour chacun le prix, la durée, le format, le positionnement et ce que disent les avis publics, chaque fait avec son lien. Termine par une carte de positionnement et le créneau à prendre. À utiliser quand l''utilisateur dit « qui sont mes concurrents », « est-ce que ce marché est encombré », « quelles formations existent déjà », « analyse concurrentielle », « trouve le créneau », ou « combien facturent les autres ».'
argument-hint: "[pays, région ou marché en ligne]"
---

# formation-concurrents

> Dans Formateur 360, chaque formation a son dossier `cours/<cours>/` ; l'étape vente écrit dans `cours/<cours>/vente/`. Remplacez `<cours>` par le nom court du cours (demandez-le s'il n'est pas clair, ou reprenez celui du dossier existant). Si `cours/<cours>/00-brief.md` existe, lisez-le : il contient public, durée, niveau et modalité.

Chaque acheteur résout déjà ce besoin d'une façon ou d'une autre. Ce skill découvre
comment, à quel prix, et ce qui lui déplaît, pour que la formation parte d'un
créneau plutôt que d'une intuition.

## Les règles

- **Sources publiques uniquement, chaque fait avec son lien.** Sites et catalogues
  d'organismes, pages de prix, plateformes de formation en ligne, sites d'avis,
  annuaires officiels de formations financées, forums, presse. Si une source est
  inaccessible, dites-le. N'inventez jamais un concurrent, un prix, une note ou un avis.
- **Lire, pas aspirer.** Lisez les pages comme une personne le ferait. Respectez les
  conditions de chaque site.
- **Citations exactes**, courtes, avec le lien. Ce sont des données d'étude, jamais
  des témoignages.
- **Comparer ce qui est comparable.** Un prix de formation n'a de sens qu'avec sa
  durée, son format (inter, intra, en ligne), la taille du groupe et ce qui est
  inclus. Ramenez toujours à un prix par participant et par jour quand c'est possible,
  et notez si le prix est HT ou TTC.

## Étape 1 : qui est là

À partir de `cours/<cours>/vente/idee.md` (écrivez-le d'abord s'il manque ; voir
`/formation-conseil` étape 0) :

| type | ce que cela veut dire | exemple pour « Animer une réunion qui décide » |
| --- | --- | --- |
| Direct | même sujet, même public, même type d'acheteur | les formations « réunions efficaces » des organismes de la région |
| Indirect | autre format pour le même besoin | coaching de managers, formation en ligne, conférence, formation interne |
| Substitut | comment l'acheteur s'en passe | un livre, une vidéo gratuite, un modèle de compte rendu, ne rien faire |

Visez 5 à 10 concurrents directs et indirects, plus les principaux substituts. Pour
chaque type d'acheteur visé (entreprise, particulier, organisme public, organisme de
formation), cherchez comme il chercherait : « formation <sujet> <ville> »,
« formation <sujet> inter-entreprises », « <sujet> formation en ligne »,
« <sujet> formation financée », et les catalogues des organismes publics du pays.

## Étape 2 : les faits

Une ligne par concurrent dans `cours/<cours>/vente/concurrents.csv` :

`nom,type,url,pays_ou_canal,format,duree_jours,taille_groupe,prix,ht_ou_ttc,prix_par_participant_jour,ce_qui_est_inclus,financement_mentionne,accroche,note,nb_avis,date_source`

`accroche` est leur propre titre ou slogan, copié. `financement_mentionne` : le
dispositif que le concurrent affiche lui-même (ne déduisez pas une éligibilité qu'il
n'affiche pas). Laissez vide ce que la source ne dit pas.

## Étape 3 : ce que disent leurs participants

Pour les 3 à 5 principaux, lisez les avis publics (plateformes de formation en ligne,
Google, sites d'avis), les plus mauvais d'abord puis les « bien, mais... ». Notez les
plaintes récurrentes par thème avec un décompte et une ou deux citations avec lien.
Marquez un thème « mince » s'il repose sur moins de trois avis. Beaucoup de
formations en entreprise n'ont pas d'avis publics : dites-le plutôt que de combler.

## Étape 4 : la carte et le créneau

Écrivez `cours/<cours>/vente/concurrents.md` :

1. Le tableau (depuis le CSV), trié du plus direct au moins direct.
2. Les prix : le plus bas, la médiane, le plus haut, par participant et par jour,
   séparément pour l'inter, l'intra et l'en ligne.
3. Une carte de positionnement en texte : deux axes qui comptent pour cet acheteur
   (prix et personnalisation, durée et preuve de résultat, théorie et pratique...),
   et où se situe chaque concurrent.
4. Les plaintes, classées, avec liens.
5. **Le créneau** : ce que personne ne fait bien et que cette formation pourrait
   faire, relié aux preuves. S'il n'y a pas de créneau, dites-le clairement : c'est
   le résultat le plus utile que ce skill puisse donner.
6. La menace : qui pourrait copier cette formation le plus vite (un organisme avec
   un catalogue et des commerciaux, souvent), et comment.

## Sortie

`cours/<cours>/vente/concurrents.csv`, `cours/<cours>/vente/concurrents.md`. Suite : `/formation-panel`
utilise les plaintes pour écrire de vraies objections ; `/formation-prix` utilise
la fourchette de prix.
