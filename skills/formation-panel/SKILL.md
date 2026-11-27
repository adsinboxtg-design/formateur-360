---
name: formation-panel
description: 'Le panel d''acheteurs. Lance un essaim de sous-agents acheteurs (100 par défaut, 20 avec --quick) tirés des acheteurs visés par la formation : responsables RH ou formation en entreprise, particuliers qui paient eux-mêmes, organismes publics, organismes de formation revendeurs, chacun avec son rôle, son budget, sa façon d''acheter et son objection. Chacun voit la même offre et décide s''il achète. Compte les taux d''achat par type d''acheteur et par segment, les raisons de refus avec leurs mots, ce qui ferait basculer un non, et les réponses de prix pour formation-prix. À utiliser quand l''utilisateur dit « est-ce que ça se vendrait », « teste ma formation sur des acheteurs », « lance le panel », « simule des clients », « qui achète ma formation », ou « valide la demande ».'
argument-hint: "[--n 100 | --quick] [--seed S]"
---

# formation-panel

> Dans Formateur 360, chaque formation a son dossier `cours/<cours>/` ; l'étape vente écrit dans `cours/<cours>/vente/`. Remplacez `<cours>` par le nom court du cours (demandez-le s'il n'est pas clair, ou reprenez celui du dossier existant). Si `cours/<cours>/00-brief.md` existe, lisez-le : il contient public, durée, niveau et modalité.

Au lieu de deviner si la formation se vendra, vous posez la question à cent
acheteurs, chacun un sous-agent qui joue un acheteur précis tiré de vos acheteurs
visés. Vous êtes l'animateur. Vous ne répondez jamais à la place d'un acheteur.

Ce que l'utilisateur a tapé après `/formation-panel` : `$ARGUMENTS`

## L'outil

Toute la comptabilité passe par `panel.py` dans le dossier de ce skill :

```bash
python3 "${CLAUDE_SKILL_DIR}/panel.py" --dir cours/<cours>/vente/panel <commande>
```

Ci-dessous, `PANEL` désigne exactement cela. Si le chemin n'est pas développé,
utilisez le dossier de base que Claude Code a affiché pour ce skill. L'état est dans
`cours/<cours>/vente/panel/`.

## Étape 1 : les acheteurs visés

Écrivez `cours/<cours>/vente/acheteurs.json` (forme : `acheteurs.exemple.json` dans ce dossier) :

- `formation`, `cible` (le public participant, en une ligne précise), `devise`.
- `unite_prix` : l'unité des questions de prix, par exemple « en euros HT par
  participant pour la journée ». Choisissez le format principal ; testez un autre
  format (intra au forfait, par exemple) dans un second panel.
- `segments` : 2 à 5 groupes, chacun avec `nom`, `type` (`entreprise`,
  `particulier`, `public` ou `organisme`), `role` (qui décide, concrètement), `part`,
  `budget` [min, max] et `budget_libelle` (ce que ce budget représente).
- `comportements` : 4 à 8 façons d'acheter, avec `part` et `comment` (compare les
  catalogues, achète sur recommandation, n'achète qu'avec un financement, fidèle à
  son organisme habituel, exige des preuves...).
- `objections` : les 4 à 8 doutes que ce type d'acheteur a réellement.
- `contextes` (facultatif) : des situations concrètes qui rendent un acheteur réel
  (plan de formation bouclé, budget réduit, incident récent...).

Appuyez-vous sur du réel : ce que l'utilisateur sait de ses acheteurs, et si
`/formation-concurrents` a tourné, les plaintes de `cours/<cours>/vente/concurrents.md`. Si
l'utilisateur a de vraies données (entretiens, évaluations, demandes reçues),
préférez-les à vos suppositions et dites quelles parties sont supposées. Montrez le
profil en quelques lignes et laissez l'utilisateur le corriger avant de distribuer :
un mauvais profil d'acheteur fausse tout le panel. Les budgets en particulier
viennent de l'utilisateur ou d'une source qu'il peut vérifier ; sinon, marquez-les
comme estimations.

## Étape 2 : l'offre

Écrivez `cours/<cours>/vente/offre-panel.md` : ce qu'un acheteur verrait vraiment dans un
courriel, une brochure ou un catalogue. Le titre, le public, le résultat promis, la
durée et le format, le prix, le formateur en une ligne, ce qui est inclus. Trois à
six lignes simples, sans superlatif, rien que la formation ne puisse tenir. Chaque
acheteur voit exactement ce texte.

## Étape 3 : distribuer et lancer

```bash
PANEL init --acheteurs cours/<cours>/vente/acheteurs.json --offre cours/<cours>/vente/offre-panel.md --n 100
PANEL prompts
```

`init` distribue les cartes (même seed, mêmes cartes ; la seed est enregistrée).
`prompts` écrit un brief par acheteur et les liste par vagues de 10. Pour chaque
vague, envoyez UN message avec un appel à l'outil Agent par acheteur de la vague
(l'outil s'appelle Task dans les anciennes versions de Claude Code) :

- `subagent_type` : `general-purpose`
- `description` : `panel <id>`
- `prompt` : `Lis <chemin du brief> et suis-le exactement. C'est toute ta consigne.`

Attendez la fin de la vague avant la suivante. Après la dernière :

```bash
PANEL check      # liste les réponses manquantes ou invalides
PANEL prompts    # réécrit les briefs de celles-là seulement ; relancez-les une fois
PANEL tally
```

Si un acheteur a affiché son JSON dans sa réponse au lieu d'écrire le fichier (ça
arrive), rangez sa propre réponse avec `PANEL save <id>` et la réponse en entrée
standard ; `save` refuse tout ce qui n'est pas une réponse valide. Un acheteur qui
échoue deux fois est écarté et compté dans les résultats. N'écrivez jamais une
réponse à la place d'un acheteur.

Avant un panel de 100, dites à l'utilisateur que cela fait 100 appels de sous-agents
et proposez `--quick` (20 acheteurs, avec `--n 20`) pour un premier aperçu. Chaque
sous-agent écrit un fichier dans `cours/<cours>/vente/panel/reponses/` ; en mode de permission
par défaut, c'est une approbation par fichier : proposez le mode « accept edits »
(Maj+Tab) pour la durée du panel.

## Étape 4 : le restituer

`PANEL tally` écrit `cours/<cours>/vente/panel/resultats.md` et `resultats.json`. Donnez :

1. Le titre : « 32 achètent · 68 refusent » et le taux d'achat.
2. Qui achète et qui n'achète pas : les types d'acheteur et segments qui diffèrent le
   plus. C'est souvent là que se trouve la décision (vendre aux RH ou aux particuliers ?).
3. Pourquoi ils refusent : les trois premières raisons, avec une citation chacune,
   telle qu'écrite.
4. Ce qui ferait basculer un non : les réponses qui reviennent le plus.
5. Une phrase sur ce qu'il faut changer avant d'investir, et quel skill le fait
   (prix, offre, marketing).

## Limites honnêtes, à dire une fois

Ce sont des acheteurs simulés. Ils sont bons pour faire apparaître des objections,
des segments et des formulations auxquels vous n'aviez pas pensé, et mauvais pour
prédire de vrais achats : les modèles de langage penchent vers la complaisance, donc
le taux d'achat est un plafond. Ils ne connaissent pas les règles réelles de
financement ni les budgets réels de vos acheteurs : ce qu'ils en disent est une
hypothèse à vérifier. Confirmez les grandes décisions avec de vrais acheteurs (une
session pilote, des pré-inscriptions, trois rendez-vous avec des responsables
formation) avant d'engager quoi que ce soit. Ne présentez jamais une citation du
panel comme un témoignage.

## Le brief de chaque acheteur

`panel.py` remplit la carte dans un modèle fixe (voir `BRIEF` dans le script) : qui
est l'acheteur (prénom, rôle, segment, type d'acheteur et ce que cela implique,
budget, façon d'acheter, contexte, objection), l'offre mot pour mot, la consigne de
ne pas être complaisant et de ne rien inventer, et le JSON exact à écrire : achète
ou non, nombre de places la première année, un code de raison, la raison avec ses
mots, l'objection principale, ce qui le ferait changer d'avis, le délai et le
circuit de décision, et quatre réponses de prix. Ne modifiez jamais un brief pour un
seul acheteur.

## Sortie

`cours/<cours>/vente/acheteurs.json`, `cours/<cours>/vente/offre-panel.md`, `cours/<cours>/vente/panel/` (cartes,
briefs, réponses, résultats). Suite : `/formation-prix` lit les réponses de prix,
`/formation-offre` et `/formation-marketing` lisent les objections.
