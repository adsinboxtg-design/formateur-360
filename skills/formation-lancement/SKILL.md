---
name: formation-lancement
description: 'Votre responsable du lancement. Construit un plan daté, étape par étape : d''abord un test réel peu coûteux (pré-inscriptions avec un prix, une session pilote payante, trois rendez-vous avec des responsables formation, une courte session en ligne gratuite qui mène à l''offre) pour que de vrais acheteurs confirment ce que le panel simulé a dit, puis le compte à rebours jusqu''à la première session avec responsables et échéances, le déroulé du jour J et les 30 jours suivants. À utiliser quand l''utilisateur dit « comment lancer ma formation », « plan de lancement », « session pilote », « quand faire la première session », « rétroplanning », ou « par où commencer ».'
argument-hint: "[date visée pour la première session]"
---

# formation-lancement

> Dans Formateur 360, chaque formation a son dossier `cours/<cours>/` ; l'étape vente écrit dans `cours/<cours>/vente/`. Remplacez `<cours>` par le nom court du cours (demandez-le s'il n'est pas clair, ou reprenez celui du dossier existant). Si `cours/<cours>/00-brief.md` existe, lisez-le : il contient public, durée, niveau et modalité.

Lancer une formation est un projet avec une date. Ce skill transforme tout le reste
du pack en plan daté, et commence par le moyen le moins cher de savoir si de vrais
acheteurs paieront, avant d'investir les jours de conception.

## Étape 1 : tester avant d'investir

Choisissez le test réel le moins coûteux qui convient, et faites-le avant d'engager
les jours de conception et les dépenses de `cours/<cours>/vente/chiffres.json` :

| acheteur principal | le test |
| --- | --- |
| entreprise ou RH | trois à cinq rendez-vous avec des responsables formation, avec le programme et le prix ; objectif : une proposition signée ou une date posée |
| particulier | une page avec le prix, la date et un bouton de pré-inscription (avec acompte si possible) |
| organisme public | un rendez-vous avec un conseiller pour connaître les conditions réelles de référencement et de financement |
| organisme de formation | une proposition de session pilote en sous-traitance |
| tous | une session pilote payante à prix de lancement, avec un nombre minimum d'inscrits |

Écrivez la ligne de réussite avant le test (par exemple : 6 pré-inscriptions payées en
trois semaines à 450 euros, ou 2 dates intra posées sur 5 rendez-vous), puis comparez
le résultat au taux d'achat du panel. Si les vrais acheteurs sont nettement en
dessous du panel, croyez les vrais acheteurs et revenez à `/formation-offre` ou
`/formation-prix`. Une seule vraie inscription payée vaut plus que le panel entier.

## Étape 2 : le compte à rebours

D'aujourd'hui à la première session, avec de vraies dates (demandez la date visée ;
par défaut, la plus proche réaliste compte tenu des délais de `cours/<cours>/vente/logistique.md`
et du temps de conception). Par blocs hebdomadaires, chaque tâche avec un responsable
et une échéance :

- Administratif et argent : ce que `cours/<cours>/vente/logistique.md` demande de vérifier ou
  d'obtenir.
- Conception : programme, supports, exercices (avec `/nouveau-cours`).
- Logistique : salle ou outil en ligne, fournisseurs réservés selon leurs délais.
- Marketing : le calendrier de `cours/<cours>/vente/marketing.md` à partir de J-30.
- La date limite d'annulation si le seuil d'inscrits n'est pas atteint.
- Une répétition (à blanc, ou devant deux personnes de confiance) avant la vraie
  session.

Marquez le chemin critique : les tâches qui décalent la date si elles glissent.

## Étape 3 : le jour J

Un déroulé heure par heure côté organisation : arrivée, vérifications, accueil, ce qui
est envoyé et quand (supports, questionnaire d'évaluation), quoi faire si quelque
chose casse (d'après le registre des risques). Le déroulé pédagogique lui-même relève
du cahier du formateur (agent `cahier-formateur`).

## Étape 4 : les 30 jours suivants

Ce qu'il faut mesurer (évaluation à chaud, comportement au poste à 30 jours, demandes
de nouvelles sessions, recommandations), le niveau qui déclenche un changement, et un
bilan à J+7 et J+30 avec les questions à se poser. Prévoyez de demander aux
participants et à l'acheteur l'autorisation d'utiliser leurs retours réels : ce
seront vos premières vraies preuves.

## Sortie

`cours/<cours>/vente/lancement.md` avec le test, le compte à rebours, le déroulé du jour J et le
bilan à 30 jours. Suite : `/formation-dossier` compile tout en un dossier de lancement.
