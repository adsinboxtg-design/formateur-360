# Apprenants simulés : profils et règles de sélection

> Fichier rédigé le 24/11/2026 à partir des instructions des agents et des skills `simulation-cours` et `validation-supports` du pack. Adaptez-le à votre pratique.

Les apprenants simulés font apparaître des problèmes probables. Ils ne remplacent pas un essai avec de vrais apprenants, ni un test avec des personnes concernées pour l'accessibilité.

## Les profils

| Agent | Cible (`plan`, `ateliers`, `supports`) | Ce qu'il révèle | À retenir quand le brief indique… |
|---|---|---|---|
| `apprenant-expert` | supports | Erreurs, imprécisions, raccourcis abusifs, informations obsolètes ; vérifie dans la documentation officielle | Des faits vérifiables (chiffres, numéros, réglementation, versions, commandes) |
| `apprenant-difficile` | supports | Contestations, questions pièges, objections à préparer | Un public critique, des enjeux sensibles, un sujet qui divise |
| `apprenant-mefoutiste` | supports | Pertes d'attention, consignes sautées, ateliers réussis sans avoir compris | Une formation obligatoire ou imposée, une motivation faible |
| `apprenant-debutant-anxieux` | plan, ateliers, supports | Prérequis implicites, jargon non défini, étapes sautées, peur d'être jugé | Des débutants, un public peu sûr de lui, un sujet réputé difficile |
| `apprenant-peu-numerique` | plan, ateliers, supports | Consignes techniques floues, manipulations supposées acquises, blocages sur poste ou en visio | Une aisance numérique faible ou inégale, du distanciel, des manipulations sur téléphone ou ordinateur |
| `apprenant-pragmatique` | plan, ateliers, supports | Théorie sans usage, absence d'outil réutilisable, transfert au poste faible | Des managers, un public pressé, une formation en entreprise |
| `apprenant-experimente-resistant` | plan, ateliers, supports | Ce qui heurte l'expérience, arguments manquants pour convaincre | Des professionnels expérimentés, une formation qui change des pratiques |
| `apprenant-non-natif` | plan, ateliers, supports | Phrases trop longues, idiomes, vocabulaire rare, sigles, références culturelles implicites | Des participants dont le français n'est pas la langue première |
| `apprenant-accessibilite` | plan, ateliers, supports | Contrastes, texte dans les images, vidéos sans sous-titres, consignes uniquement orales ou visuelles, manipulations difficiles | Un besoin d'accessibilité connu, ou un public large et inconnu (lancer avec un besoin précis : dyslexie, malvoyance, malentendance ou mobilité réduite des mains) |
| `apprenant-dynamique-groupe` | surtout plan et ateliers | Bavard qui monopolise, silencieux qui disparaît, travaux de groupe mal cadrés, timing qui explose | Du travail en groupe, des restitutions, des questions à toute la salle, un timing serré |
| `apprenant-simule` | plan, ateliers | Décrochage d'un profil précis de niveau, de modalité ou de matériel | Une contrainte précise (« ingénieur, distanciel, Windows sans droits admin ») |

`avocat-du-diable` n'est pas un apprenant : `simulation-cours` le lance toujours sur le plan ou les ateliers.

## Règles de sélection

1. Lire la section « Public apprenant » de `00-brief.md` : participants, expérience, motivation, aisance numérique, langue, besoins d'accessibilité connus, dynamique de groupe.
2. Retenir **3 à 5 profils** marqués pour la cible. Au-delà, les retours se recoupent et le coût augmente.
3. Un profil par signal du brief : chaque profil retenu doit répondre à une information du brief. Annoncer au formateur la raison de chaque choix ; il peut ajouter ou retirer un profil.
4. Cible `supports` : `apprenant-expert` est retenu dès que le sujet comporte des faits vérifiables.
5. `apprenant-accessibilite` : un besoin par lancement. Pour vérifier deux besoins, lancer deux fois.
6. Sans section « Public apprenant » renseignée : le dire, proposer de la compléter, et à défaut lancer `apprenant-expert`, `apprenant-difficile` et `apprenant-mefoutiste` sur les supports, ou `apprenant-debutant-anxieux` et `apprenant-dynamique-groupe` sur le plan.
7. Après une première série, ne relancer que les profils dont les constats ont donné lieu à une correction, plus un profil nouveau si le public a changé.
