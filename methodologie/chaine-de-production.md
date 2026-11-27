# Chaîne de production d'un cours

| # | Étape | Agent | Livrable |
|---|---|---|---|
| 1 | Cadrage | `cadrage` | `00-brief.md` |
| 2 | Recherche documentaire | `documentaliste` | `01-notes/sources.md`, notes |
| 3 | Veille vidéo | `veille-video` | `01-notes/videos/*.md` |
| 4 | Tri des notes | `trieur-notes` | notes classées, sujets envoyés en `bibliotheque/` |
| 5 | Plan | `planificateur` | `02-plan.md` |
| 6 | Simulation (plan) | `avocat-du-diable` + 3 à 5 apprenants choisis selon `profils/apprenants.md` (skill `simulation-cours`) | `simulations/plan-*.md` |
| 7 | Ateliers | `concepteur-ateliers` | `04-ateliers/` |
| 8 | Supports | `redacteur-supports` | `03-supports/` (pptx, pdf, cheatsheet) |
| 9 | Cahier formateur | `cahier-formateur` | `05-formateur/cahier.md` |
| 10 | Évaluations & feedback | `evaluations` (+ skill `export-google-forms`) | `06-evaluations/`, Google Forms en ligne |
| 11 | Simulation (ateliers) | `avocat-du-diable` + 3 à 5 apprenants choisis selon `profils/apprenants.md` (skill `simulation-cours`) | `simulations/ateliers-*.md` |
| 12 | Validation des supports | 3 à 5 apprenants choisis selon `profils/apprenants.md` (skill `validation-supports`) | `simulations/supports-*.md` |
| 13 | Jury d'experts | `jury-ingenierie`, `jury-cognition`, `jury-andragogie`, `jury-evaluation`, `jury-inclusion` (skill `jury-experts`, grille `profils/jury.md`) | `jury/notes.md`, `jury/deliberation.md` |
| 14 | Relecture finale | `relecteur` | `07-relecture.md` |

Étapes 8 à 10 : les fichiers Office/PDF sont produits par la skill `production-documents` puis vérifiés par `controle-visuel` (le markdown reste la source).

Chaque étape ajoute ses décisions dans `journal.md`.
Tu valides à la fin des étapes 1, 5, 6, 12, 13 et 14 avant de continuer.
