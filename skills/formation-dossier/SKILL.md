---
name: formation-dossier
description: 'Votre planificateur. Compile tout ce que les autres skills du pack ont écrit (avis du conseil, concurrents, panel d''acheteurs, prix, offre, chiffres du CFO, marketing, logistique, lancement) en un dossier de lancement unique, avec en tête un verdict calculé à partir des chiffres et jamais écrit à la main : Rentable, Pas encore (avec les chiffres qui échouent) ou Incomplet. Ajoute une synthèse et une page unique pour un partenaire, un financeur ou un organisme. À utiliser quand l''utilisateur dit « fais le dossier », « rassemble tout », « est-ce que ma formation est rentable », « donne-moi le plan », ou à la fin du pack.'
argument-hint: "[--taux-min 0.25]"
---

# formation-dossier

> Dans Formateur 360, chaque formation a son dossier `cours/<cours>/` ; l'étape vente écrit dans `cours/<cours>/vente/`. Remplacez `<cours>` par le nom court du cours (demandez-le s'il n'est pas clair, ou reprenez celui du dossier existant). Si `cours/<cours>/00-brief.md` existe, lisez-le : il contient public, durée, niveau et modalité.

La dernière étape. Un document sur lequel le formateur peut agir, ou qu'il peut
remettre à un partenaire, un organisme ou un financeur, construit uniquement à partir
de ce que le pack a trouvé.

Outil dans ce dossier :

```bash
python3 "${CLAUDE_SKILL_DIR}/compile.py" --dir cours/<cours>/vente
```

## Étape 1 : voir ce qui existe

```bash
python3 "${CLAUDE_SKILL_DIR}/compile.py" --dir cours/<cours>/vente --check
```

affiche le verdict et chaque contrôle. Les contrôles, tous calculés :

1. Chaque format rapporte de l'argent au remplissage prévu (`cours/<cours>/vente/chiffres.json`).
2. Le seuil de participants tient dans la capacité, quand une capacité est donnée.
3. L'année 1 dégage un résultat positif après coûts fixes et lancement.
4. Le gain par jour mobilisé sur l'année, conception comprise, atteint la cible du
   formateur, quand une cible est donnée.
5. Assez d'acheteurs simulés achètent (`cours/<cours>/vente/panel/resultats.json` ; seuil par
   défaut 25 %, modifiable avec `--taux-min`, en disant pourquoi).

S'il n'y a pas de chiffres, le verdict est Incomplet : proposez `/formation-cfo`.
Listez les autres sections manquantes avec le skill qui remplit chacune. Ne remplissez
jamais vous-même une section manquante à partir de suppositions.

## Étape 2 : la synthèse

Écrivez `cours/<cours>/vente/synthese.md`, une demi-page, en mots simples :

- Ce qu'est la formation et pour qui, en deux phrases.
- Le verdict et les trois chiffres derrière (gain par jour mobilisé, seuil de
  participants, résultat de l'année 1).
- Sur quoi le panel et le conseil sont d'accord, et où ils divergent.
- Le plus gros risque et ce qui sera fait.
- Ce qu'il faut pour démarrer (jours de conception et dépenses selon le CFO, le premier
  test réel selon le lancement).
- La seule chose à faire cette semaine.

Si le verdict est Pas encore, la synthèse commence par ce qui doit changer et par quel
skill. N'adoucissez jamais un contrôle qui échoue.

## Étape 3 : compiler

```bash
python3 "${CLAUDE_SKILL_DIR}/compile.py" --dir cours/<cours>/vente
```

écrit `cours/<cours>/vente/dossier.md` : titre, verdict et contrôles, tableau des chiffres clés,
l'idée, puis chaque section produite par le pack, et ce qui n'est pas encore fait.

## Étape 4 : la page unique

Écrivez `cours/<cours>/vente/une-page.md` pour quelqu'un qui décide en deux minutes : le
problème, le public et l'acheteur, l'offre et le prix, le tableau des chiffres, les
preuves (résultat du panel, créneau face aux concurrents, tout test réel), ce qui est
demandé. Mêmes chiffres que le dossier, mot pour mot.

## Règles

- Le verdict vient de `compile.py`. N'écrivez jamais Rentable à la main, et n'arrondissez
  jamais un chiffre qui échoue en un chiffre qui passe.
- Dites une fois, clairement : le panel est composé d'acheteurs simulés et les chiffres
  sont des projections ; de vrais acheteurs et de vrais devis les confirment. Ce n'est
  pas un conseil financier, juridique ou fiscal.
- Si l'utilisateur veut un PDF, un document partageable ou une présentation,
  proposez de l'exporter, mais gardez le markdown comme référence.

## Sortie

`cours/<cours>/vente/synthese.md`, `cours/<cours>/vente/dossier.md`, `cours/<cours>/vente/une-page.md`. Donnez
ensuite le verdict en une ligne et la seule chose à faire cette semaine. Si le verdict
est Rentable, proposez `/nouveau-cours` (la conception, dans Formateur 360) pour
concevoir la formation.
