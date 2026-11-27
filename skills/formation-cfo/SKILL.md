---
name: formation-cfo
description: Votre directeur financier pour une formation. Calcule, avant la première session, ce que rapporte une session dans chaque format (inter, intra, en ligne, sous-traitance), le nombre de participants à partir duquel elle couvre ses coûts, ce que le formateur gagne réellement par jour mobilisé (préparation, déplacement et conception compris) comparé à son taux journalier cible, le résultat de l'année 1, et ce qui se passe si le prix baisse, si les sessions se remplissent moins ou s'il y a deux fois moins de sessions. Chaque nombre se rattache à une entrée vérifiable. À utiliser quand l'utilisateur dit « est-ce rentable », « fais les comptes », « seuil de rentabilité », « combien de participants minimum », « combien je gagne par jour », « ça vaut le coup de la concevoir ».
argument-hint: "[chemin de chiffres.json]"
---

# formation-cfo

> Dans Formateur 360, chaque formation a son dossier `cours/<cours>/` ; l'étape vente écrit dans `cours/<cours>/vente/`. Remplacez `<cours>` par le nom court du cours (demandez-le s'il n'est pas clair, ou reprenez celui du dossier existant). Si `cours/<cours>/00-brief.md` existe, lisez-le : il contient public, durée, niveau et modalité.

Celui qui demande « et ça coûte combien ? ». Pour un formateur, le coût principal
n'est presque jamais la salle : c'est son propre temps. Une formation qui « rapporte
3 000 euros » mais mobilise quatre jours entre préparation, déplacement et suivi ne
vaut pas ce qu'elle semble. Ce skill le montre, chaque nombre rattaché à une entrée.

Outil dans ce dossier :

```bash
python3 "${CLAUDE_SKILL_DIR}/economie.py" cours/<cours>/vente/chiffres.json --out cours/<cours>/vente/cfo.md
```

## Étape 1 : rassembler les entrées

Écrivez `cours/<cours>/vente/chiffres.json` (forme : `exemple.json` dans ce dossier). Il faut :

| champ | ce qu'on y met |
| --- | --- |
| `taux_journalier_cible` | ce que le formateur veut gagner par jour mobilisé (son tarif de consultant, ou ce qu'il gagnerait ailleurs) |
| `jours_conception` | jours pour concevoir la formation, une seule fois |
| `lancement` | dépenses uniques : maquette des supports, page de présentation, matériel |
| `fixes_annuels` | coûts annuels quel que soit le nombre de sessions : assurance, outils, certification |
| `formats` | une entrée par façon de vendre : inter (prix par participant), intra (prix par session), en ligne, sous-traitance pour un organisme |

Pour chaque format : `mode` (`participant` ou `session`), `prix` HT, `duree_jours`,
`participants_prevus`, `capacite`, `sessions_annee_1`, `commission_pct` (part
prélevée par un organisme ou une plateforme), `jours_prep_par_session` (préparation,
déplacement, administratif, suivi), `couts_par_participant` (supports, repas,
attestation) et `couts_par_session` (salle, déplacement, matériel, co-animation).

D'où viennent les nombres, dans cet ordre :

1. Les devis, factures, grilles tarifaires et contrats de l'utilisateur.
2. Des prix publics vérifiables (tarif d'une salle, d'une plateforme, d'un
   imprimeur). Notez la source à côté du nombre dans `cours/<cours>/vente/cfo-sources.md`.
3. Votre estimation, clairement marquée comme telle, avec le raisonnement. Ne
   présentez jamais une estimation comme un fait.

Demandez à l'utilisateur ce que lui seul sait : son taux journalier cible, le temps
réel qu'il passe à préparer une session, les sessions qu'il pense vraiment vendre.
Prenez les prix de `cours/<cours>/vente/prix.md` ou `cours/<cours>/vente/offre-panel.md` s'ils existent.

**Le nombre de sessions et le remplissage sont là où les plans mentent.** Si le panel
a tourné, comparez avec son taux d'achat et ses places déclarées
(`cours/<cours>/vente/panel/resultats.md`) et dites comment vous l'avez fait. Une première
année réaliste compte souvent moins de sessions que prévu.

## Étape 2 : lancer le calcul

```bash
python3 "${CLAUDE_SKILL_DIR}/economie.py" cours/<cours>/vente/chiffres.json --out cours/<cours>/vente/cfo.md
```

Il écrit, pour chaque format : le chiffre d'affaires d'une session, la commission,
les coûts directs, ce qui reste, les jours mobilisés, le gain par jour mobilisé, le
seuil de participants pour couvrir les coûts et celui pour atteindre la cible
journalière. Puis l'année 1 : chiffre d'affaires, résultat après coûts fixes et
lancement, jours mobilisés conception comprise, gain par jour sur l'année, et un
tableau « et si » (prix -10 %, remplissage -30 %, moitié des sessions). Il signale
une session déficitaire, un seuil au-delà de la capacité, une année 1 en perte et un
gain par jour sous la cible.

Scénarios sans modifier le fichier :

```bash
python3 "${CLAUDE_SKILL_DIR}/economie.py" cours/<cours>/vente/chiffres.json --prix 1.1
python3 "${CLAUDE_SKILL_DIR}/economie.py" cours/<cours>/vente/chiffres.json --remplissage 0.7 --sessions 0.5
```

## Étape 3 : la note du CFO

Ajoutez en tête de `cours/<cours>/vente/cfo.md` une courte section, en mots simples :

- **Ce que vous gagnez par jour** : par format et sur l'année, conception comprise,
  face à la cible.
- **Le format qui porte l'activité** et celui qui la dilue (souvent la sous-traitance :
  pas de vente à faire, mais un gain par jour bas).
- **La ligne à surveiller** : l'hypothèse qui fait le plus bouger le résultat (souvent
  le nombre de sessions ou le remplissage de l'inter), avec le scénario qui le prouve.
- **Trois façons d'améliorer**, chacune avec le nombre qu'elle change et de combien
  (lancez le scénario, ne devinez pas).
- Si les conditions financières du conseil (`cours/<cours>/vente/conseil.md`) sont remplies.

## Règles

- Chaque nombre de votre note vient de la sortie de l'outil ou d'une entrée que vous
  pouvez nommer.
- Les prix sont hors taxes ; dites si le marché de l'utilisateur ajoute une TVA et si
  la formation professionnelle y est exonérée ou non : c'est à vérifier auprès d'une
  source officielle ou d'un comptable, selon le pays.
- Ce n'est pas un conseil financier, fiscal ou juridique. Dites une fois qu'un
  comptable doit vérifier le statut, les cotisations et la fiscalité.

## Sortie

`cours/<cours>/vente/chiffres.json`, `cours/<cours>/vente/cfo.md`, `cours/<cours>/vente/cfo-sources.md`. Suite :
`/formation-dossier` utilise ces chiffres pour le verdict ; `/formation-prix` si le
gain par jour est trop bas.
