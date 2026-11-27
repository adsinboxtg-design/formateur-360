#!/usr/bin/env python3
"""Sensibilité au prix (Van Westendorp) pour formation-prix. Bibliothèque standard uniquement.

Chaque acheteur du panel répond à quatre questions : à quel prix la formation
paraîtrait trop bon marché pour être sérieuse, une bonne affaire, chère, et trop
chère pour l'acheter. Mises ensemble, ces quatre réponses donnent une fourchette de
prix acceptable et le prix qui laisse le moins de monde mécontent.

    python3 van_westendorp.py formation/panel/reponses
    python3 van_westendorp.py prix.csv --out formation/prix-courbe.md
    python3 van_westendorp.py formation/panel/reponses --prix 450 --devise EUR

Entrée : le dossier des réponses du panel (un JSON par acheteur, écrit par
formation-panel) ou un CSV avec les colonnes trop_bas, bonne_affaire, cher,
trop_cher (une ligne par répondant, issue d'un vrai sondage de préférence). Un
répondant à qui il manque un des quatre nombres, ou qui les donne dans le désordre,
est écarté et compté.

Les quatre points :

    PMC  prix plancher        en dessous, trop de gens trouvent la formation trop bon marché
    PME  prix plafond         au-dessus, trop de gens la trouvent trop chère
    OPP  prix optimal         autant de « trop bon marché » que de « trop cher »
    IPP  prix d'indifférence  autant de « bonne affaire » que de « cher »

De PMC à PME : la fourchette acceptable. Avec des acheteurs simulés, elle sert à
choisir ce qu'on TESTE, puis on teste avec de vrais acheteurs.

Repris de founder-pricing (founder-skill, Jake Schincariol, licence MIT), traduit et
adapté aux réponses de formation-panel.
"""

import argparse
import csv
import glob
import json
import os
import sys

KEYS = ("too_cheap", "cheap", "expensive", "too_expensive")
CLES_PANEL = ("prix_trop_bas", "prix_bonne_affaire", "prix_cher", "prix_trop_cher")
CLES_CSV = ("trop_bas", "bonne_affaire", "cher", "trop_cher")


class PricingError(Exception):
    pass


def _f(v):
    try:
        x = float(str(v).replace("$", "").replace("€", "").replace("EUR", "").replace(" ", "").replace(",", ".").strip())
    except (TypeError, ValueError):
        return None
    return x if x > 0 else None


def read(path):
    """Return (rows, dropped) where rows are (too_cheap, cheap, expensive, too_expensive)."""
    raw = []
    if os.path.isdir(path):
        for fp in sorted(glob.glob(os.path.join(path, "*.json"))):
            try:
                with open(fp, encoding="utf-8") as fh:
                    a = json.load(fh)
            except (json.JSONDecodeError, UnicodeDecodeError):
                raw.append(None)
                continue
            if any(k in a for k in CLES_PANEL):
                raw.append(tuple(_f(a.get(k)) for k in CLES_PANEL))
            else:
                raw.append(tuple(_f(a.get("price_" + k)) for k in KEYS))
    elif path.endswith(".csv"):
        with open(path, newline="", encoding="utf-8") as fh:
            for r in csv.DictReader(fh):
                cles = CLES_CSV if any(k in r for k in CLES_CSV) else KEYS
                raw.append(tuple(_f(r.get(k)) for k in cles))
    else:
        raise PricingError("donnez le dossier des réponses du panel ou un .csv")
    rows, dropped = [], 0
    for r in raw:
        if r is None or any(v is None for v in r) or not (r[0] <= r[1] <= r[2] <= r[3]):
            dropped += 1
            continue
        rows.append(r)
    return rows, dropped


def curves(rows, grid):
    n = float(len(rows))
    tc = [sum(1 for r in rows if r[0] >= p) / n for p in grid]          # too cheap at p (falls)
    ch = [sum(1 for r in rows if r[1] >= p) / n for p in grid]          # a bargain at p (falls)
    ex = [sum(1 for r in rows if r[2] <= p) / n for p in grid]          # expensive at p (rises)
    te = [sum(1 for r in rows if r[3] <= p) / n for p in grid]          # too expensive at p (rises)
    return tc, ch, ex, te


def cross(grid, falling, rising):
    """First price where the rising curve meets the falling one (linear interpolation)."""
    for i in range(1, len(grid)):
        d0 = rising[i - 1] - falling[i - 1]
        d1 = rising[i] - falling[i]
        if d0 <= 0 <= d1 and d1 != d0:
            t = -d0 / (d1 - d0)
            return grid[i - 1] + t * (grid[i] - grid[i - 1])
        if d0 == 0:
            return grid[i - 1]
    return None


def analyse(rows, step=None):
    if len(rows) < 5:
        raise PricingError("il faut au moins 5 réponses complètes (reçu %d)" % len(rows))
    lo = min(r[0] for r in rows)
    hi = max(r[3] for r in rows)
    step = step or max(0.01, round((hi - lo) / 400, 2))
    grid, p = [], lo
    while p <= hi + 1e-9:
        grid.append(round(p, 4))
        p += step
    tc, ch, ex, te = curves(rows, grid)
    not_cheap = [1 - v for v in ch]
    not_exp = [1 - v for v in ex]
    pts = {
        "PMC": cross(grid, tc, not_cheap),
        "PME": cross(grid, not_exp, te),
        "OPP": cross(grid, tc, te),
        "IPP": cross(grid, ch, ex),
    }
    return {"n": len(rows), "points": pts, "range": [pts["PMC"], pts["PME"]],
            "median": {k: sorted(r[i] for r in rows)[len(rows) // 2] for i, k in enumerate(KEYS)}}


def report(res, dropped, price=None, devise="EUR"):
    m = lambda v: "n/d" if v is None else "%s %s" % ("{:,.0f}".format(v).replace(",", " ") if v >= 100 else ("%.2f" % v).replace(".", ","), devise)
    p = res["points"]
    L = ["# Sensibilité au prix", "",
         "%d réponses complètes%s. Acheteurs simulés : cela sert à choisir ce qu'on teste, pas à trancher." % (
             res["n"], (", %d écartées (incomplètes ou dans le désordre)" % dropped) if dropped else ""), "",
         "| point | prix | signification |", "| --- | ---: | --- |",
         "| PMC | %s | en dessous, trop d'acheteurs trouvent la formation trop bon marché pour être sérieuse |" % m(p["PMC"]),
         "| OPP | %s | autant de « trop bon marché » que de « trop cher » : la moindre résistance |" % m(p["OPP"]),
         "| IPP | %s | autant de « bonne affaire » que de « cher » |" % m(p["IPP"]),
         "| PME | %s | au-dessus, trop d'acheteurs la trouvent trop chère pour l'acheter |" % m(p["PME"]), "",
         "**Fourchette acceptable : %s à %s.**" % (m(p["PMC"]), m(p["PME"])), ""]
    md = res["median"]
    L.append("Réponses médianes : trop bon marché %s, bonne affaire %s, cher %s, trop cher %s." % (
        m(md["too_cheap"]), m(md["cheap"]), m(md["expensive"]), m(md["too_expensive"])))
    if price is not None and p["PMC"] is not None and p["PME"] is not None:
        where = "dans" if p["PMC"] <= price <= p["PME"] else ("sous" if price < p["PMC"] else "au-dessus de")
        L += ["", "Votre prix actuel, %s, est **%s** la fourchette acceptable." % (m(price), where)]
    return "\n".join(L) + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("source", help="le dossier des réponses du panel, ou un CSV")
    ap.add_argument("--prix", "--price", dest="price", type=float, help="votre prix actuel, pour le situer dans la fourchette")
    ap.add_argument("--devise", default="EUR")
    ap.add_argument("--out", help="écrire le rapport ici (markdown)")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    try:
        rows, dropped = read(a.source)
        res = analyse(rows)
    except (PricingError, FileNotFoundError) as e:
        print("erreur : %s" % e, file=sys.stderr)
        return 2
    if a.json:
        print(json.dumps(dict(res, dropped=dropped), indent=1))
        return 0
    text = report(res, dropped, a.price, a.devise)
    if a.out:
        with open(a.out, "w", encoding="utf-8") as fh:
            fh.write(text)
        print("écrit : %s" % a.out)
    else:
        sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
