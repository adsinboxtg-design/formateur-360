#!/usr/bin/env python3
"""Délibération du jury d'experts de Formateur 360. Bibliothèque standard uniquement, aucun accès réseau.

Lit les notes que chaque membre du jury a écrites dans jury/<membre>.json et applique
les règles de profils/jury.md, sans rien interpréter :

    critères 1 à 8   la note du membre principal du domaine
    critères 9 et 10 la moyenne de tous les membres, arrondie à l'entier inférieur

    Validé                 aucune note inférieure à 3 et moyenne d'au moins 4
    Validé sous réserve    aucune note de 1
    À retravailler         au moins une note de 1, ou au moins trois critères sous 3

Si un membre principal manque, ses critères sont « non évalués » et la décision est
marquée provisoire.

    python3 deliberation.py --dir cours/<cours>/jury
    python3 deliberation.py --dir cours/<cours>/jury --json
"""

import argparse
import glob
import json
import math
import os
import sys

CRITERES = {
    1: ("Alignement objectifs, activités, évaluations", "ingenierie"),
    2: ("Objectifs observables et niveau cognitif adapté", "ingenierie"),
    3: ("Charge cognitive, séquençage, densité des supports", "cognition"),
    4: ("Pratique active, récupération, espacement, retour", "cognition"),
    5: ("Prise en compte des adultes", "andragogie"),
    6: ("Conditions du transfert au poste", "andragogie"),
    7: ("Validité des évaluations et niveaux couverts", "evaluation"),
    8: ("Inclusion et accessibilité", "inclusion"),
    9: ("Exactitude et sources", None),
    10: ("Faisabilité et cohérence avec la promesse", None),
}
MEMBRES = ("ingenierie", "cognition", "andragogie", "evaluation", "inclusion")


class JuryError(Exception):
    pass


def lire(d):
    notes = {}
    for path in sorted(glob.glob(os.path.join(d, "*.json"))):
        try:
            with open(path, encoding="utf-8") as fh:
                obj = json.load(fh)
        except (json.JSONDecodeError, UnicodeDecodeError):
            raise JuryError("%s n'est pas un JSON valide" % os.path.basename(path))
        if not isinstance(obj, dict) or "membre" not in obj:
            continue  # autre fichier JSON du dossier
        m = obj["membre"]
        if m not in MEMBRES:
            raise JuryError("membre inconnu dans %s : %r" % (os.path.basename(path), m))
        n = obj.get("notes") or {}
        propres = {}
        for c in CRITERES:
            v = n.get(str(c), n.get(c))
            if not isinstance(v, int) or isinstance(v, bool) or not 1 <= v <= 5:
                raise JuryError("%s : la note du critère %d doit être un entier de 1 à 5 (reçu %r)" % (m, c, v))
            propres[c] = v
        notes[m] = propres
    if not notes:
        raise JuryError("aucune note de membre dans %s" % d)
    return notes


def deliberer(notes):
    retenues = {}
    for c, (_, principal) in CRITERES.items():
        if principal is None:
            vals = [n[c] for n in notes.values()]
            retenues[c] = int(math.floor(sum(vals) / len(vals)))
        else:
            retenues[c] = notes[principal][c] if principal in notes else None
    evaluees = [v for v in retenues.values() if v is not None]
    moyenne = sum(evaluees) / len(evaluees)
    if any(v == 1 for v in evaluees) or sum(1 for v in evaluees if v < 3) >= 3:
        decision = "À retravailler"
    elif all(v >= 3 for v in evaluees) and moyenne >= 4:
        decision = "Validé"
    else:
        decision = "Validé sous réserve"
    manquants = [m for m in MEMBRES if m not in notes]
    provisoire = any(v is None for v in retenues.values())
    # écarts : un critère où deux membres divergent d'au moins 2 points
    ecarts = []
    for c in CRITERES:
        vals = {m: n[c] for m, n in notes.items()}
        if len(vals) > 1 and max(vals.values()) - min(vals.values()) >= 2:
            ecarts.append((c, vals))
    return {"retenues": retenues, "moyenne": moyenne, "decision": decision, "provisoire": provisoire,
            "membres": sorted(notes), "manquants": manquants, "ecarts": ecarts}


def rapport(notes, r):
    L = ["# Délibération du jury : notes et décision calculée", "",
         "**Décision : %s%s**" % (r["decision"], " (provisoire : jury incomplet)" if r["provisoire"] else ""),
         "", "Moyenne des critères évalués : %s / 5. Membres : %s.%s" % (
             ("%.1f" % r["moyenne"]).replace(".", ","), ", ".join(r["membres"]),
             (" Absents : %s." % ", ".join(r["manquants"])) if r["manquants"] else ""), "",
         "| # | Critère | " + " | ".join(r["membres"]) + " | note retenue |",
         "| ---: | --- |" + " ---: |" * len(r["membres"]) + " ---: |"]
    for c, (lib, _) in CRITERES.items():
        v = r["retenues"][c]
        L.append("| %d | %s | %s | %s |" % (c, lib, " | ".join(str(notes[m][c]) for m in r["membres"]),
                                           "non évalué" if v is None else "**%d**" % v))
    if r["ecarts"]:
        L += ["", "## Désaccords à arbitrer (écart d'au moins 2 points)", ""]
        for c, vals in r["ecarts"]:
            L.append("- Critère %d (%s) : %s." % (c, CRITERES[c][0], ", ".join("%s %d" % kv for kv in sorted(vals.items()))))
    L += ["", "_Jury simulé. La décision applique les règles de profils/jury.md aux notes des membres ; elle ne remplace"
          " pas l'avis de vrais experts ni l'essai avec de vrais apprenants._"]
    return "\n".join(L) + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--dir", default="jury")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--out", help="par défaut : <dir>/notes.md")
    a = ap.parse_args(argv)
    try:
        notes = lire(a.dir)
        r = deliberer(notes)
    except JuryError as e:
        print("erreur : %s" % e, file=sys.stderr)
        return 2
    if a.json:
        print(json.dumps(r, ensure_ascii=False, indent=1))
        return 0
    out = a.out or os.path.join(a.dir, "notes.md")
    with open(out, "w", encoding="utf-8") as fh:
        fh.write(rapport(notes, r))
    print("Décision : %s%s. Écrit : %s" % (r["decision"], " (provisoire)" if r["provisoire"] else "", out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
