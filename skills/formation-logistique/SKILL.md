---
name: formation-logistique
description: 'Votre responsable des opérations pour une formation. Détermine comment la formation se déroule concrètement : lieux et salles (ou outils de visio), matériel, supports et impressions, co-animation, inscriptions, convocations, facturation, attestations et évaluations, les obligations administratives et les certifications ou agréments à vérifier selon le pays et le type d''acheteur, et un registre des risques avec la parade pour chacun. Renvoie les coûts réels au CFO. À utiliser quand l''utilisateur dit « comment l''organiser », « logistique », « quelle salle », « qu''est-ce qu''il me faut », « certification », « agrément », « Qualiopi », « facturation », ou « le jour J ».'
argument-hint: "[pays ou région]"
---

# formation-logistique

> Dans Formateur 360, chaque formation a son dossier `cours/<cours>/` ; l'étape vente écrit dans `cours/<cours>/vente/`. Remplacez `<cours>` par le nom court du cours (demandez-le s'il n'est pas clair, ou reprenez celui du dossier existant). Si `cours/<cours>/00-brief.md` existe, lisez-le : il contient public, durée, niveau et modalité.

Un plan qui tient sur le papier peut échouer un lundi à 8 h 45 devant un
vidéoprojecteur qui ne s'allume pas. Ce skill s'assure que la première session peut
vraiment avoir lieu, et que les chiffres du CFO incluent ce qu'elle coûte réellement.

Le cahier du formateur de la partie conception (agent `cahier-formateur` :
installations, vérifications, plan B) couvre la préparation pédagogique de la salle : ne le refaites
pas, renvoyez-y et concentrez-vous ici sur l'organisation commerciale et
administrative.

## Étape 1 : le cycle d'une session

À partir de `cours/<cours>/vente/idee.md`, `cours/<cours>/vente/offre.md` et `cours/<cours>/vente/chiffres.json`,
écrivez le cycle d'une session, de la vente au suivi : proposition et devis,
inscription, convention ou bon de commande, convocation, questionnaire préalable,
préparation, session, évaluation à chaud, attestation, facture, suivi à 30 jours,
évaluation à froid. Marquez ce que l'acheteur voit, et qui fait quoi.

## Étape 2 : lieux, outils et fournisseurs

Pour chaque coût du CFO et chaque besoin matériel : deux ou trois fournisseurs réels
que l'utilisateur peut contacter (salles, traiteur, imprimeur, plateforme
d'inscription, outil de visio, outil de facturation), leurs prix publics ou la façon
d'obtenir un devis, les délais de réservation et les conditions d'annulation. Liens à
l'appui. Quand seul un devis peut répondre, dites-le et ajoutez-le aux questions
ouvertes. Si un prix réel diffère de `cours/<cours>/vente/chiffres.json`, mettez-le à jour et
dites que le CFO doit relancer le calcul.

## Étape 3 : les personnes

Qui anime, qui co-anime, qui gère l'administratif. Si un co-animateur intervient : son
tarif (donné par l'utilisateur) et ce qu'il prend en charge. Le temps de
l'utilisateur hors animation, session par session : il alimente
`jours_prep_par_session` du CFO.

## Étape 4 : les routines

Des routines courtes et numérotées pour les moments qui font ou défont la formation :
la veille de la session, l'accueil, un incident technique, un participant en
difficulté ou en désaccord, la clôture, la facturation et le suivi. Chacune tient sur
une page.

## Étape 5 : obligations, certifications et financements à vérifier

Une liste de ce qui s'applique habituellement à ce type de formation, **dans le pays
de l'utilisateur et de ses acheteurs**, chaque point avec la page officielle pour le
confirmer : statut et enregistrement du formateur ou de l'organisme, TVA sur la
formation professionnelle, assurance responsabilité civile professionnelle, documents
contractuels attendus, certification qualité exigée par certains financeurs, agréments
ou référencements nécessaires pour qu'un acheteur utilise un dispositif de
financement public, accessibilité aux personnes en situation de handicap, protection
des données des participants.

Les règles diffèrent selon le pays et la région et changent souvent. Ne déduisez
jamais qu'une formation est éligible à un financement : écrivez ce qu'il faut vérifier
et où. Dites clairement que l'utilisateur doit confirmer chaque point auprès de
l'administration compétente ou d'un professionnel. Ce n'est pas un conseil juridique.

## Étape 6 : registre des risques

Les dix choses les plus susceptibles de mal tourner (session annulée faute
d'inscrits, formateur malade, salle indisponible, panne technique, participant qui ne
correspond pas au public, facture impayée, mauvaise évaluation), chacune avec sa
probabilité, sa gravité et la parade. Fixez en particulier le **seuil d'annulation** :
le nombre minimum d'inscrits et la date limite pour décider, à partir du seuil du CFO.

## Sortie

`cours/<cours>/vente/logistique.md`, et `cours/<cours>/vente/chiffres.json` mis à jour si des coûts réels
ont changé. Suite : `/formation-lancement`.
