---
name: formation-prix
description: 'Trouve le prix que les acheteurs paieront vraiment pour une formation. Transforme les quatre réponses de prix du panel en une fourchette acceptable (méthode Van Westendorp : trop bon marché, bonne affaire, cher, trop cher), la confronte à ce que facturent réellement les concurrents et à ce que le formateur doit gagner par jour, puis recommande un prix par format (inter, intra, en ligne, sous-traitance), une gamme et une offre de lancement à tester. À utiliser quand l''utilisateur dit « combien je facture », « quel prix pour ma formation », « est-ce que X euros c''est trop cher », « tarif intra », « prix par participant », « stratégie de prix », ou après le panel.'
argument-hint: "[prix actuel]"
---

# formation-prix

> Dans Formateur 360, chaque formation a son dossier `cours/<cours>/` ; l'étape vente écrit dans `cours/<cours>/vente/`. Remplacez `<cours>` par le nom court du cours (demandez-le s'il n'est pas clair, ou reprenez celui du dossier existant). Si `cours/<cours>/00-brief.md` existe, lisez-le : il contient public, durée, niveau et modalité.

Le prix est le levier le plus rapide sur ce que vous gagnez, et celui que les
formateurs devinent le plus. Ce skill le fixe à partir de trois choses vérifiables :
ce que disent les acheteurs, ce que facturent les concurrents, et ce que vous devez
gagner par jour mobilisé.

Outil dans ce dossier :

```bash
python3 "${CLAUDE_SKILL_DIR}/van_westendorp.py" cours/<cours>/vente/panel/reponses --prix 450 --devise EUR --out cours/<cours>/vente/prix-courbe.md
```

## Étape 1 : ce que disent les acheteurs

Si `/formation-panel` a tourné, chaque acheteur a répondu à quatre questions de prix,
dans l'unité de `cours/<cours>/vente/acheteurs.json` (`unite_prix`). Lancez l'outil sur
`cours/<cours>/vente/panel/reponses` (ou sur un CSV de vrai sondage avec les colonnes
`trop_bas, bonne_affaire, cher, trop_cher`, toujours préférable à des réponses
simulées). Il donne :

| point | signification |
| --- | --- |
| PMC | en dessous, trop d'acheteurs trouvent la formation trop bon marché pour être sérieuse |
| OPP | le prix qui rencontre le moins de résistance dans les deux sens |
| IPP | autant d'acheteurs la trouvent une bonne affaire que chère |
| PME | au-dessus, trop d'acheteurs ne l'achèteront pas |

De PMC à PME : la fourchette acceptable. Regardez aussi les réponses par type
d'acheteur dans `cours/<cours>/vente/panel/resultats.md` : un particulier et un service RH ne
réagissent pas au même prix. Si le panel n'a pas tourné, dites-le et proposez
`/formation-panel --quick` d'abord. N'inventez pas de fourchette.

## Étape 2 : ce que facturent les concurrents

Depuis `cours/<cours>/vente/concurrents.md` (ou en les cherchant maintenant, sur leurs propres
pages de prix, avec liens) : le prix des formations les plus proches. Ramenez tout à
un prix par participant et par jour, en précisant HT ou TTC, inter ou intra, et ce
qui est inclus.

## Étape 3 : ce que la formation doit rapporter

Depuis `cours/<cours>/vente/chiffres.json` : les coûts par session et par participant, et le
`taux_journalier_cible` du formateur. Lancez l'outil du CFO à deux ou trois prix
candidats (coefficient sur tous les formats) :

```bash
python3 "${CLAUDE_SKILL_DIR}/../formation-cfo/economie.py" cours/<cours>/vente/chiffres.json --prix 1.1
```

Pour un prix précis d'un seul format, copiez `chiffres.json`, changez ce prix et
relancez. Le chiffre qui compte : le gain par jour mobilisé, préparation comprise,
comparé à la cible.

## Étape 4 : décider

Écrivez `cours/<cours>/vente/prix.md` :

1. **Le prix de chaque format**, et pourquoi : où il se situe dans la fourchette,
   face aux concurrents, et le gain par jour mobilisé qu'il donne (sorti de l'outil,
   pas deviné). Rappelez la cohérence entre formats : un intra au forfait doit rester
   intéressant face à N participants en inter.
2. **La gamme**, si elle a du sens : par exemple une version courte, la version
   standard, et une version avec accompagnement après la formation, chaque marche
   avec une raison d'y monter.
3. **L'offre de lancement** : un prix ou un bonus pour la session pilote, avec une
   date de fin, qui n'habitue pas les acheteurs à attendre une remise.
4. **Ce qu'il faut tester avec de vrais acheteurs** : deux prix dans la fourchette et
   comment les tester (deux propositions à deux prospects, pré-inscriptions à chaque prix).
5. Les objections de prix du panel, telles qu'écrites (les trois premières), pour que
   le marketing y réponde.

## Règles

- Les réponses d'acheteurs simulés servent à choisir ce qu'on teste. Ce ne sont pas
  des preuves.
- Ne fixez jamais un prix sous le seuil de rentabilité d'une session sans le dire,
  ni sans dire combien de temps le CFO estime que c'est tenable.
- Pas de faux prix barré : jamais de « au lieu de X » pour un prix jamais pratiqué.
- Si un financeur public ou un dispositif impose un plafond de prix, il vient d'une
  source officielle que l'utilisateur peut vérifier, avec le lien.

## Sortie

`cours/<cours>/vente/prix-courbe.md`, `cours/<cours>/vente/prix.md`. Si un prix change, mettez à jour
`cours/<cours>/vente/chiffres.json` et relancez `/formation-cfo`. Suite : `/formation-offre`.
