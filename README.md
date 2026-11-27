# Formateur 360

Un plugin Claude pour mener une formation de l'idée à la première session, en trois temps :

1. **Vendre** : vérifier que la formation se vendra et qu'elle rapportera (conseil, concurrents, panel d'acheteurs simulés, prix, offre, comptes, marketing, logistique, lancement, dossier final avec verdict).
2. **Concevoir** : cadrage, recherche documentaire sourcée, plan avec fil rouge, ateliers, supports à votre charte, cahier du formateur, évaluations.
3. **Faire valider** : apprenants simulés choisis selon votre public, puis jury d'experts simulés qui note le cours sur une grille commune.

## Installer

Dans Claude Code :

```
/plugin marketplace add adsinboxtg-design/formateur-360
/plugin install formateur-360@formateur-360-marketplace
```

Ou installez le fichier `formateur-360.plugin` si on vous l'a transmis.

## Démarrer

1. Installez le plugin.
2. Ouvrez un dossier vide qui servira d'espace de travail (vos cours, votre profil, vos chartes y seront rangés).
3. Lancez `/init-espace`, puis `/premiere-utilisation` : vérification des outils, des connecteurs Google, création de votre profil de formateur (ton, vocabulaire) et de votre charte.
4. Ensuite, `/formateur-360` vous dit où en est un cours et quelle commande lancer.

Le parcours complet est décrit dans `methodologie/formateur-360.md`.

## Principes

- **Rien d'inventé** : toute affirmation technique s'appuie sur une adresse réellement consultée, consignée dans `01-notes/sources.md` ; le reste est marqué `[À VÉRIFIER]`.
- **Votre voix** : aucun texte pour les apprenants n'est rédigé sans votre profil de formateur.
- **Vous décidez** : les apprenants simulés et le jury proposent ; chaque correction est retenue ou rejetée par vous, et notée dans `journal.md`.
- **Simulé n'est pas réel** : apprenants, acheteurs et jury simulés font apparaître des problèmes probables. Ils ne remplacent ni de vrais participants, ni de vrais pairs, ni un test avec des personnes concernées pour l'accessibilité.
- **Coût** : un panel de 100 acheteurs, une validation à 5 apprenants ou un jury complet lancent de nombreux sous-agents. Des versions rapides existent (`--quick`, `--rapide`).

## À savoir

- Données de vos cours : gardez votre espace de travail privé (dépôt Git privé si vous en utilisez un).
- `profils/jury.md` contient des références bibliographiques classiques listées de mémoire : vérifiez-les avant toute citation publique.
- Les scripts de production (pptx, docx, Google Forms) demandent Python et les dépendances de `scripts/requirements.txt` ; `/premiere-utilisation` les vérifie.

## Crédits

- Vente, jury d'experts, apprenants simulés supplémentaires et orchestration : Thomas Gendera.
- Conception (cadrage, recherche, plan, ateliers, supports, cahier formateur, évaluations, premiers apprenants simulés, scripts et modèles) : contributions externes, intégrées avec l’accord de leur auteur.

## Licence

MIT (voir `LICENSE`), pour l'ensemble du plugin, partie conception comprise.
