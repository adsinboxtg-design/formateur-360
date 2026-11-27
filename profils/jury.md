# Jury d'experts : membres, cadres, grille et règles

> Fichier rédigé le 24/11/2026 à partir de la skill `jury-experts`, des cinq agents du jury et du script `deliberation.py`, qui applique les règles ci-dessous. Si vous modifiez les critères ou les règles, modifiez aussi le script.

Le jury est **simulé**. Ses cinq membres sont fictifs : docteurs et chercheurs, trente ans d'expérience en formation, coordination et pédagogie. Aucun ne porte le nom d'un chercheur réel, ne parle au nom de quelqu'un ni ne s'invente de titre ou de publication. Le jury fait apparaître des problèmes probables au regard de cadres publiés ; il ne remplace ni l'avis de vrais pairs ni l'essai avec de vrais apprenants.

## Membres

| Identifiant | Spécialité | Section des cadres | Critères principaux |
|---|---|---|---|
| `ingenierie` | Ingénierie pédagogique | Ingénierie pédagogique | 1, 2 |
| `cognition` | Sciences cognitives de l'apprentissage | Sciences cognitives de l'apprentissage | 3, 4 |
| `andragogie` | Formation des adultes et transfert | Formation des adultes et transfert | 5, 6 |
| `evaluation` | Évaluation | Évaluation | 7 |
| `inclusion` | Inclusion et accessibilité | Inclusion et accessibilité | 8 |

Chaque membre note les dix critères, en restant prudent hors de son domaine.

## Cadres par section

Un membre ne cite que les références de sa section ci-dessous, ou une source qu'il a réellement ouverte, avec son adresse. Sans confirmation possible : « à vérifier ».

> Références classiques listées de mémoire lors de la rédaction de ce fichier, non revérifiées une à une : contrôlez-les avant toute citation dans un document public.

### Ingénierie pédagogique
- Alignement pédagogique : Biggs, J. (1996). Enhancing teaching through constructive alignment. *Higher Education*, 32, 347-364.
- Taxonomie de Bloom révisée : Anderson, L. W. et Krathwohl, D. R. (dir.) (2001). *A Taxonomy for Learning, Teaching, and Assessing*. Longman.

### Sciences cognitives de l'apprentissage
- Charge cognitive : Sweller, J. (1988). Cognitive load during problem solving: Effects on learning. *Cognitive Science*, 12, 257-285.
- Apprentissage multimédia : Mayer, R. E. (2009). *Multimedia Learning* (2e éd.). Cambridge University Press.
- Récupération : Roediger, H. L. et Karpicke, J. D. (2006). Test-enhanced learning. *Psychological Science*, 17(3), 249-255.
- Retour : Hattie, J. et Timperley, H. (2007). The power of feedback. *Review of Educational Research*, 77(1), 81-112.

### Formation des adultes et transfert
- Andragogie : Knowles, M. S. (1980). *The Modern Practice of Adult Education*. Cambridge Book Company.
- Transfert : Baldwin, T. T. et Ford, J. K. (1988). Transfer of training: A review and directions for future research. *Personnel Psychology*, 41, 63-105.
- Niveaux 3 et 4 : Kirkpatrick, D. L. et Kirkpatrick, J. D. (2006). *Evaluating Training Programs: The Four Levels* (3e éd.). Berrett-Koehler.

### Évaluation
- Évaluation formative : Black, P. et Wiliam, D. (1998). Assessment and classroom learning. *Assessment in Education*, 5(1), 7-74.
- Niveaux évalués : Kirkpatrick et Kirkpatrick (2006), ci-dessus.
- Alignement de l'évaluation : Biggs (1996), ci-dessus.

### Inclusion et accessibilité
- Conception universelle de l'apprentissage : CAST, Universal Design for Learning Guidelines, https://udlguidelines.cast.org/
- Contraste des textes : W3C, WCAG, critère 1.4.3 Contrast (Minimum), https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html (repère pour les écrans ; à vérifier en projection réelle).

## Grille commune (notes entières de 1 à 5)

| # | Critère | Note retenue |
|---:|---|---|
| 1 | Alignement objectifs, activités, évaluations | membre `ingenierie` |
| 2 | Objectifs observables et niveau cognitif adapté | membre `ingenierie` |
| 3 | Charge cognitive, séquençage, densité des supports | membre `cognition` |
| 4 | Pratique active, récupération, espacement, retour | membre `cognition` |
| 5 | Prise en compte des adultes | membre `andragogie` |
| 6 | Conditions du transfert au poste | membre `andragogie` |
| 7 | Validité des évaluations et niveaux couverts | membre `evaluation` |
| 8 | Inclusion et accessibilité | membre `inclusion` |
| 9 | Exactitude et sources | moyenne des cinq membres, arrondie à l'entier inférieur |
| 10 | Faisabilité et cohérence avec la promesse | moyenne des cinq membres, arrondie à l'entier inférieur |

Échelle : 1 = défaut grave qui compromet l'apprentissage ; 2 = insuffisant ; 3 = acceptable avec corrections ; 4 = bon ; 5 = exemplaire.

Exigences : toute note inférieure à 4 s'appuie sur une preuve (fichier et passage) ; chaque critique est accompagnée d'une correction réalisable dans la durée du brief ; une préférence personnelle n'est pas un défaut.

## Règles de décision (appliquées par `deliberation.py`)

- **Validé** : aucune note retenue inférieure à 3 et moyenne d'au moins 4.
- **Validé sous réserve** : aucune note retenue de 1.
- **À retravailler** : au moins une note de 1, ou au moins trois critères sous 3.
- Membre principal absent (mode `--rapide`) : ses critères sont « non évalués » et la décision est provisoire.
- Désaccord signalé : un écart d'au moins 2 points entre deux membres sur un même critère.
