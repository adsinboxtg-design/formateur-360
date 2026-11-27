---
name: jury-experts
description: Réunit un jury d'experts simulés de niveau docteur et chercheur (trente ans d'expérience en formation, coordination et pédagogie) pour évaluer un cours complet sur une grille commune fondée sur des cadres scientifiques publiés (alignement pédagogique, Bloom révisé, charge cognitive, apprentissage multimédia, andragogie, transfert, évaluation formative, Kirkpatrick, conception universelle de l'apprentissage). Cinq membres notent avec preuves, une décision est calculée, le président rédige la délibération et les corrections exigées. À utiliser quand l'utilisateur dit « jury d'experts », « fais évaluer mon cours », « avis d'experts », « valide ma formation », « audit pédagogique », ou après la validation des supports.
argument-hint: "[nom du cours] [--rapide]"
---

# jury-experts

Le dernier regard avant la relecture finale. Là où les apprenants simulés disent « je bloque ici », le jury dit « ce cours atteint-il ses objectifs, au regard de ce que la recherche sait de l'apprentissage ? ».

Ce que l'utilisateur a tapé après `/jury-experts` : `$ARGUMENTS`

## Étape 0 : prérequis

Lisez `profils/jury.md` (membres, cadres, grille, règles de décision). Vérifiez que `cours/<cours>/` contient au moins `00-brief.md`, `02-plan.md` et `03-supports/`. S'il manque les ateliers ou les évaluations, dites-le : les critères correspondants seront notés sur ce qui existe, et le jury le signalera. Ne lancez pas le jury sur un cours sans plan ni supports.

## Étape 1 : le dossier du jury

Écrivez `cours/<cours>/jury/dossier.md` : la liste des fichiers que le jury doit lire, et rien d'autre. Incluez `00-brief.md`, `02-plan.md`, `03-supports/`, `04-ateliers/`, `05-formateur/cahier.md`, `06-evaluations/`, `01-notes/sources.md`, les synthèses `simulations/*-synthese.md` et `simulations/supports-expert.md` si elles existent, et `vente/offre.md` s'il existe (pour vérifier que le cours tient la promesse vendue). N'incluez ni `journal.md` ni aucun historique de conception : le jury juge ce qui est livré.

## Étape 2 : réunir le jury

Lancez en UN SEUL message (outil Agent), sans l'historique de conception, les cinq membres : `jury-ingenierie`, `jury-cognition`, `jury-andragogie`, `jury-evaluation`, `jury-inclusion`. Consigne à chacun : `Dossier du cours : cours/<cours>/. Lis cours/<cours>/jury/dossier.md et profils/jury.md, puis écris ton avis dans cours/<cours>/jury/<ton identifiant>.md et tes notes dans cours/<cours>/jury/<ton identifiant>.json, comme décrit dans tes instructions.`

Avec `--rapide`, ne lancez que `jury-ingenierie`, `jury-cognition` et `jury-evaluation`, et dites que la décision sera provisoire. Avant le jury complet, dites au formateur qu'il s'agit de cinq sous-agents qui lisent tout le cours.

## Étape 3 : la décision calculée

```bash
python3 "${CLAUDE_SKILL_DIR}/deliberation.py" --dir cours/<cours>/jury
```

Le script vérifie les notes, applique les règles de `profils/jury.md` et écrit `jury/notes.md` : tableau des notes par membre, note retenue par critère, décision (Validé, Validé sous réserve, À retravailler, éventuellement provisoire) et désaccords d'au moins deux points. Si un fichier de notes est invalide, relancez le membre concerné une fois ; n'écrivez jamais une note à sa place.

## Étape 4 : la délibération du président

Lisez les cinq avis et écrivez `cours/<cours>/jury/deliberation.md` :

1. **La décision**, telle que calculée par le script, et la moyenne. Ne la modifiez pas.
2. **Les corrections exigées**, fusionnées et dédoublonnées, classées par impact sur l'apprentissage ; pour chacune : le critère, la preuve (fichier, passage), la correction, le membre qui la demande. Les points soulevés par plusieurs membres en tête.
3. **Les désaccords** : pour chaque écart signalé par le script, les deux positions et l'argument de chacune. Gardez-les ; ne tranchez à la place du formateur que si un cadre de `profils/jury.md` le permet clairement, en citant lequel.
4. **Ce qui est réussi** : ce que plusieurs membres saluent.
5. **Recommandation du président** : en deux phrases, la priorité absolue avant de délivrer la formation.

## Étape 5 : décision du formateur

Présentez la délibération. Pour chaque correction exigée : retenue ou rejetée, avec la raison. Reportez les décisions dans `journal.md`. Ne modifiez les supports qu'après décision ; les corrections retenues passent ensuite par les agents de conception habituels, puis par la relecture finale (`relecteur`).

## Règles

- Les membres sont fictifs. Personne ne parle au nom d'un chercheur réel, et aucune référence n'est inventée.
- Une note sans preuve sous 4 n'est pas recevable : renvoyez l'avis au membre une fois.
- Dites une fois, clairement : c'est un jury simulé qui fait apparaître des problèmes probables au regard de cadres publiés. Il ne remplace pas l'avis de vrais pairs ni l'essai avec de vrais apprenants.

## Sortie

`cours/<cours>/jury/` : `dossier.md`, un avis et un fichier de notes par membre, `notes.md`, `deliberation.md`. Donnez la décision en une ligne et les trois corrections prioritaires.
