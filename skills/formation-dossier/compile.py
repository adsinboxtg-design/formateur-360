#!/usr/bin/env python3
"""Compile le dossier de lancement pour formation-dossier. Bibliothèque standard uniquement, aucun accès réseau.

Lit tout ce que les autres skills du pack ont écrit dans formation/ et assemble un
document, formation/dossier.md, avec un verdict en tête. Le verdict est calculé à
partir des chiffres, jamais écrit à la main :

    Rentable     chaque contrôle qui a des données passe
    Pas encore   au moins un contrôle échoue (chaque échec est listé avec son chiffre)
    Incomplet    il n'y a pas encore de chiffres (lancez d'abord formation-cfo)

Les contrôles :
    1. chaque format rapporte de l'argent au remplissage prévu       (formation/chiffres.json)
    2. le seuil de participants tient dans la capacité, si elle est donnée
    3. l'année 1 dégage un résultat positif après coûts fixes et lancement
    4. le gain par jour mobilisé atteint la cible du formateur, si elle est donnée
    5. assez d'acheteurs du panel achètent   (formation/panel/resultats.json, --taux-min, 25 % par défaut)

    python3 compile.py                          # lit ./formation, écrit ./formation/dossier.md
    python3 compile.py --dir chemin/formation --taux-min 0.3
    python3 compile.py --check                  # affiche le verdict ; code 0 si Rentable, 1 sinon

Adapté de founder-plan (founder-skill, Jake Schincariol, licence MIT).
"""

import argparse
import importlib.util
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SECTIONS = [  # (fichier dans formation/, titre, skill qui l'écrit)
    ("synthese.md", "Synthèse", "formation-dossier"),
    ("conseil.md", "L'avis du conseil", "formation-conseil"),
    ("concurrents.md", "La concurrence", "formation-concurrents"),
    ("panel/resultats.md", "Le panel d'acheteurs", "formation-panel"),
    ("prix.md", "Le prix", "formation-prix"),
    ("offre.md", "L'offre", "formation-offre"),
    ("cfo.md", "Les chiffres", "formation-cfo"),
    ("marketing.md", "Le marketing", "formation-marketing"),
    ("logistique.md", "La logistique", "formation-logistique"),
    ("lancement.md", "Le lancement", "formation-lancement"),
]


def _charger_economie():
    path = os.path.join(HERE, "..", "formation-cfo", "economie.py")
    spec = importlib.util.spec_from_file_location("formation_economie", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _lire(path):
    try:
        with open(path, encoding="utf-8") as fh:
            return fh.read().strip()
    except FileNotFoundError:
        return None


def _sans_h1(text):
    lines = text.splitlines()
    if lines and lines[0].startswith("# "):
        lines = lines[1:]
    return "\n".join(("#" + l) if l.startswith("#") else l for l in lines).strip()


def verdict(d, taux_min=0.25):
    """Renvoie (verdict, controles, chiffres, panel). controles = [(ok, texte)]."""
    eco = _charger_economie()
    m = eco.argent
    controles = []
    chiffres = panel = None
    raw = _lire(os.path.join(d, "chiffres.json"))
    if raw:
        chiffres = eco.analyser(json.loads(raw))
        dev = chiffres["devise"]
        for f in chiffres["formats"]:
            c = f["contribution_session"]
            controles.append((c > 0, "%s : une session au remplissage prévu laisse %s après ses coûts directs." % (f["nom"], m(c, dev))
                              if c > 0 else "%s : une session au remplissage prévu PERD %s." % (f["nom"], m(-c, dev))))
            s, cap = f["seuil_participants"], f["capacite"]
            if s is not None and cap is not None:
                ok = not math.isinf(s) and s <= cap
                controles.append((ok, "%s : il faut %s participants pour couvrir les coûts d'une session, pour une capacité de %s." % (
                    f["nom"], "une infinité de" if math.isinf(s) else "%d" % s, eco._g(cap))))
        r = chiffres["resultat_annee"]
        controles.append((r > 0, "Résultat de l'année 1 après coûts fixes et lancement : %s." % m(r, dev) if r > 0
                          else "L'année 1 PERD %s après coûts fixes et lancement." % m(-r, dev)))
        if chiffres["taux_cible"] and chiffres["par_jour_annee"] is not None:
            pj, t = chiffres["par_jour_annee"], chiffres["taux_cible"]
            controles.append((pj >= t, "Gagné par jour mobilisé sur l'année, conception comprise : %s, pour une cible de %s." % (m(pj, dev), m(t, dev))))
    raw = _lire(os.path.join(d, "panel", "resultats.json"))
    if raw:
        panel = json.loads(raw)
        t = panel["taux_achat"]
        controles.append((t >= taux_min, "%d acheteurs simulés sur %d achètent (%.0f %%, le seuil est %.0f %%)." % (
            panel["achats"], panel["repondu"], t * 100, taux_min * 100)))
    if chiffres is None:
        v = "Incomplet"
    elif all(ok for ok, _ in controles):
        v = "Rentable"
    else:
        v = "Pas encore"
    return v, controles, chiffres, panel


def compiler(d, taux_min=0.25):
    eco = _charger_economie()
    idee = _lire(os.path.join(d, "idee.md"))
    nom = None
    if idee:
        first = idee.splitlines()[0]
        nom = first[2:].strip() if first.startswith("# ") else None
    v, controles, ch, panel = verdict(d, taux_min)
    titre = nom or (ch["formation"] if ch and ch.get("formation") else "Votre formation")
    L = ["# %s · Dossier de lancement" % titre, "", "**Verdict : %s**" % v, ""]
    for ok, text in controles:
        L.append("- %s %s" % ("✓" if ok else "✗", text))
    if v == "Incomplet":
        L.append("- Pas encore de chiffres. Lancez /formation-cfo, puis recompilez.")
    L.append("")
    if ch:
        m = lambda x: eco.argent(x, ch["devise"])
        L += ["| chiffre clé | |", "| --- | ---: |"]
        for f in ch["formats"]:
            L.append("| %s : prix | %s %s |" % (f["nom"], m(f["prix"]), "par participant" if f["mode"] == "participant" else "par session"))
            L.append("| %s : gagné par jour mobilisé | %s |" % (f["nom"], m(f["par_jour"])))
        L += ["| Chiffre d'affaires année 1 | %s |" % m(ch["ca_annee"]),
              "| Résultat année 1 | %s |" % m(ch["resultat_annee"]),
              "| Jours mobilisés année 1 (conception comprise) | %s |" % eco._g(ch["jours_total"])]
        if ch["par_jour_annee"] is not None:
            L.append("| Gagné par jour mobilisé sur l'année | %s |" % m(ch["par_jour_annee"]))
        if panel:
            L.append("| Panel d'acheteurs | %d achètent · %d refusent |" % (panel["achats"], panel["refus"]))
        L.append("")
    if idee:
        L += ["## L'idée", "", _sans_h1(idee), ""]
    manque = []
    for fname, heading, skill in SECTIONS:
        text = _lire(os.path.join(d, fname))
        if text:
            L += ["## %s" % heading, "", _sans_h1(text), ""]
        else:
            manque.append((heading, skill))
    if manque:
        L += ["## Pas encore fait", ""] + ["- %s : lancez /%s" % hs for hs in manque] + [""]
    L.append("_Le panel est composé d'acheteurs simulés et les chiffres sont des projections à partir de vos entrées."
             " Confirmez la demande avec de vrais acheteurs et les coûts avec de vrais devis avant d'investir."
             " Ce n'est pas un conseil financier, juridique ou fiscal._")
    return v, "\n".join(L) + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--dir", default="formation")
    ap.add_argument("--taux-min", type=float, default=0.25)
    ap.add_argument("--check", action="store_true", help="affiche seulement le verdict ; code 0 si Rentable")
    ap.add_argument("--out", help="par défaut : <dir>/dossier.md")
    a = ap.parse_args(argv)
    if not os.path.isdir(a.dir):
        print("erreur : pas de dossier %s/ ici. Lancez d'abord les autres skills du pack." % a.dir, file=sys.stderr)
        return 2
    try:
        v, text = compiler(a.dir, a.taux_min)
        if a.check:
            _, controles, _, _ = verdict(a.dir, a.taux_min)
            print("Verdict : %s" % v)
            for ok, t in controles:
                print("  %s %s" % ("✓" if ok else "✗", t))
            return 0 if v == "Rentable" else 1
    except Exception as e:  # message lisible plutôt qu'une trace Python
        print("erreur : %s" % e, file=sys.stderr)
        return 2
    out = a.out or os.path.join(a.dir, "dossier.md")
    with open(out, "w", encoding="utf-8") as fh:
        fh.write(text)
    print("Verdict : %s. Écrit : %s" % (v, out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
