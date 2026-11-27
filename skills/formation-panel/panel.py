#!/usr/bin/env python3
"""Le panel d'acheteurs de formation-panel. Bibliothèque standard uniquement, aucun accès réseau.

Il tient la comptabilité d'un essaim d'acheteurs simulés : il distribue une carte
par acheteur à partir du profil des acheteurs (type d'acheteur, rôle, budget,
façon d'acheter, objection), écrit un brief par acheteur pour un sous-agent, vérifie
les réponses et fait le décompte de qui achète, qui n'achète pas, et pourquoi.

    python3 panel.py init --acheteurs formation/acheteurs.json --offre formation/offre-panel.md [--n 100] [--seed 7]
    python3 panel.py prompts [--wave 10]     # un brief par acheteur restant, par vagues
    python3 panel.py check                   # réponses manquantes ou invalides
    python3 panel.py save P003 < reponse.txt # range le JSON qu'un acheteur a affiché au lieu de l'écrire
    python3 panel.py tally [--out formation/panel/resultats.md]
    python3 panel.py status

État dans formation/panel/ (--dir pour changer) : panel.json, cartes.json,
briefs/<id>.md, reponses/<id>.json, resultats.md, resultats.json.

L'outil ne répond jamais à la place d'un acheteur. Chaque nombre de resultats.md est
compté dans les fichiers de réponse écrits par les sous-agents. Des acheteurs simulés
servent à trouver vite et pour pas cher les objections et les points faibles. Ce ne
sont pas des clients : confirmez l'essentiel avec de vrais acheteurs.

Adapté de founder-consumer (founder-skill, Jake Schincariol, licence MIT).
"""

import argparse
import json
import os
import random
import sys

PRENOMS = [
    "Camille", "Julien", "Sophie", "Karim", "Nathalie", "Mamadou", "Isabelle", "Thomas", "Aïcha", "Laurent",
    "Émilie", "Youssef", "Valérie", "Pierre", "Fatou", "Nicolas", "Chantal", "Mehdi", "Céline", "Olivier",
    "Mélanie", "Jean-François", "Sarah", "Benoît", "Nadia", "Stéphane", "Awa", "Philippe", "Inès", "Marc",
    "Geneviève", "Rachid", "Claire", "Didier", "Amina", "Sébastien", "Marie-Ève", "Patrick", "Samira", "Luc",
    "Audrey", "Moussa", "Hélène", "François", "Yasmine", "Vincent", "Delphine", "Serge", "Lina", "Christophe",
    "Anne-Sophie", "Ibrahima", "Véronique", "David", "Salomé", "Kevin", "Mireille", "Hugo", "Leïla", "Bruno",
    "Pascale", "Ousmane", "Caroline", "Arnaud", "Myriam", "Frédéric", "Josée", "Antoine", "Khadija", "Éric",
    "Martine", "Adrien", "Sylvie", "Guillaume", "Mariama", "Alexandre", "Corinne", "Simon", "Rania", "Gilles",
    "Laetitia", "Mathieu", "Nicole", "Yannick", "Zoé", "Jérôme", "Brigitte", "Maxime", "Hawa", "Cédric",
    "Sandrine", "Louis", "Danielle", "Fabien", "Noémie", "Thierry", "Agnès", "Romain", "Mounia", "Alain",
    "Florence", "Jonathan", "Assia", "Raphaël", "Manon", "Christian", "Lucie", "Bastien", "Coralie", "Quentin",
]
TYPES = {
    "entreprise": "Vous décidez pour une organisation (entreprise, service RH ou formation), avec son budget, ses priorités et son circuit de validation. Vous devez pouvoir justifier la dépense en interne.",
    "particulier": "Vous payez avec votre propre argent, sur votre temps personnel, sauf si un financement que vous connaissez déjà s'applique.",
    "public": "Vous achetez pour un organisme public ou parapublic. Vous avez des règles d'achat, des critères d'éligibilité et des publics à servir ; vous ne pouvez pas tout acheter de gré à gré.",
    "organisme": "Vous êtes un organisme de formation qui pourrait sous-traiter ou revendre cette formation. Vous raisonnez en marge, en remplissage de sessions, en cohérence avec votre catalogue et en risque de réputation.",
}
RAISONS = ["prix", "budget", "besoin", "confiance", "contenu", "format", "calendrier", "financement", "deja_couvert", "autre"]
CHAMPS = {"id", "achete", "code_raison", "raison"}
PRIX = ("prix_trop_bas", "prix_bonne_affaire", "prix_cher", "prix_trop_cher")
VAGUE = 10


class PanelError(Exception):
    pass


# ── distribution des cartes ─────────────────────────────────────────────────────
def _quota(items, n, key="part"):
    """Répartit n selon les parts, exactement (plus grand reste)."""
    total = sum(float(it.get(key, 1)) for it in items) or 1.0
    raw = [n * float(it.get(key, 1)) / total for it in items]
    counts = [int(r) for r in raw]
    order = sorted(range(len(items)), key=lambda i: raw[i] - counts[i], reverse=True)
    for i in order[: n - sum(counts)]:
        counts[i] += 1
    return counts


def valider_acheteurs(c):
    for k in ("formation", "cible", "unite_prix", "segments", "comportements", "objections"):
        if k not in c or c[k] in ("", [], None):
            raise PanelError("acheteurs.json doit contenir '%s'" % k)
    for s in c["segments"]:
        for k in ("nom", "type", "role", "budget"):
            if k not in s:
                raise PanelError("chaque segment doit avoir nom, type, role et budget [min, max] (manque '%s')" % k)
        if s["type"] not in TYPES:
            raise PanelError("type de segment %r inconnu ; valeurs possibles : %s" % (s["type"], ", ".join(TYPES)))
        if len(s["budget"]) != 2:
            raise PanelError("le budget du segment %r doit être [min, max]" % s["nom"])
    for b in c["comportements"]:
        if "nom" not in b:
            raise PanelError("chaque comportement doit avoir un nom")


def distribuer(acheteurs, n=100, seed=7):
    """Distribue n cartes. Mêmes acheteurs + n + seed = mêmes cartes, à chaque fois."""
    valider_acheteurs(acheteurs)
    if n < 1:
        raise PanelError("--n doit valoir au moins 1")
    rng = random.Random(seed)
    segs = []
    for s, k in zip(acheteurs["segments"], _quota(acheteurs["segments"], n)):
        segs += [s] * k
    comps = []
    for b, k in zip(acheteurs["comportements"], _quota(acheteurs["comportements"], n)):
        comps += [b] * k
    rng.shuffle(segs)
    rng.shuffle(comps)
    noms = PRENOMS[:]
    rng.shuffle(noms)
    while len(noms) < n:
        noms += ["%s %d" % (x, len(noms) // len(PRENOMS) + 1) for x in PRENOMS]
    objections = acheteurs["objections"]
    contextes = acheteurs.get("contextes") or []
    cartes = []
    for i in range(n):
        s, b = segs[i], comps[i]
        lo, hi = float(s["budget"][0]), float(s["budget"][1])
        pas = 100 if hi - lo >= 2000 else 10
        cartes.append({
            "id": "P%03d" % (i + 1),
            "prenom": noms[i],
            "segment": s["nom"],
            "type": s["type"],
            "role": s["role"],
            "budget": int(round(rng.uniform(lo, hi) / pas) * pas),
            "budget_libelle": s.get("budget_libelle", "budget disponible pour ce type de formation"),
            "comportement": b["nom"],
            "comportement_comment": b.get("comment", ""),
            "objection": objections[rng.randrange(len(objections))],
            "contexte": contextes[rng.randrange(len(contextes))] if contextes else "",
        })
    return cartes


# ── état ───────────────────────────────────────────────────────────────────────
def _path(d, *p):
    return os.path.join(d, *p)


def _read_json(path):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def _write_json(path, obj):
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(obj, fh, indent=1, ensure_ascii=False)
        fh.write("\n")


def init(d, acheteurs_path, offre_path, n=100, seed=None):
    try:
        acheteurs = _read_json(acheteurs_path)
    except FileNotFoundError:
        raise PanelError("fichier introuvable : %s" % acheteurs_path)
    try:
        with open(offre_path, encoding="utf-8") as fh:
            offre = fh.read().strip()
    except FileNotFoundError:
        raise PanelError("fichier introuvable : %s (écrivez d'abord l'offre : quoi, pour qui, durée, format, prix)" % offre_path)
    if not offre:
        raise PanelError("l'offre est vide")
    if seed is None:
        seed = random.SystemRandom().randrange(1, 10 ** 6)
    cartes = distribuer(acheteurs, n, seed)
    _write_json(_path(d, "panel.json"), {"n": n, "seed": seed, "acheteurs": acheteurs, "offre": offre})
    _write_json(_path(d, "cartes.json"), cartes)
    os.makedirs(_path(d, "briefs"), exist_ok=True)
    os.makedirs(_path(d, "reponses"), exist_ok=True)
    return cartes


def load_state(d):
    try:
        return _read_json(_path(d, "panel.json")), _read_json(_path(d, "cartes.json"))
    except FileNotFoundError:
        raise PanelError("aucun panel dans %s : lancez d'abord init" % d)


BRIEF = """Vous êtes un acheteur simulé dans un panel. Un formateur veut savoir, avant d'investir du temps et de l'argent, si de vrais acheteurs comme vous achèteraient sa formation. Votre réponse n'est utile que si elle est honnête : la plupart des acheteurs n'achètent pas la plupart des formations qu'on leur propose, et un oui poli est pire qu'un non clair.

=== QUI VOUS ÊTES ===
{prenom}. {role}. Segment : {segment}.
{type_texte}
Votre {budget_libelle} : environ {budget_txt} {devise}.
Votre façon d'acheter : {comportement}. {comportement_comment}
{contexte_ligne}Ce qui vous vient d'abord à l'esprit face à une offre de ce genre : « {objection} »
Vous faites partie de ce public : {cible}.
=== FIN ===

=== CE QUI VOUS EST PROPOSÉ (vous le découvrez pour la première fois, comme dans un courriel, une brochure ou une page web) ===
{offre}
=== FIN ===

Décidez comme {prenom} le ferait, avec ce budget, ces contraintes et ces doutes, dans une semaine normale. Ne soyez pas complaisant. N'inventez aucun fait sur le formateur ou la formation au-delà de ce qui est écrit ci-dessus.

Créez le fichier {out} avec votre outil d'écriture de fichiers (ne vous contentez pas d'afficher la réponse) contenant UNIQUEMENT ce JSON, sans bloc markdown, rien d'autre :
{{
  "id": "{id}",
  "achete": true ou false,
  "places": nombre de participants ou d'inscriptions que vous achèteriez la première année (0 si vous n'achetez pas),
  "code_raison": une valeur parmi {raisons},
  "raison": "pourquoi, en une ou deux phrases, avec vos mots",
  "objection": "le doute qui pèse le plus pour vous, avec vos mots",
  "ce_qui_me_ferait_changer": "la seule chose qui inverserait votre réponse, ou vide",
  "delai_decision": "combien de temps il vous faudrait pour décider et qui doit valider",
  "prix_trop_bas": le prix ({unite_prix}) en dessous duquel la formation vous semblerait trop bon marché pour être sérieuse (un nombre),
  "prix_bonne_affaire": le prix ({unite_prix}) qui vous semblerait une bonne affaire (un nombre),
  "prix_cher": le prix ({unite_prix}) à partir duquel cela devient cher, mais où vous pourriez encore acheter (un nombre),
  "prix_trop_cher": le prix ({unite_prix}) auquel vous n'achèteriez pas du tout (un nombre)
}}
"""


def write_briefs(d, wave=VAGUE):
    state, cartes = load_state(d)
    a = state["acheteurs"]
    todo = []
    for c in cartes:
        out = _path(d, "reponses", c["id"] + ".json")
        if _reponse_ok(out, c["id"]) is None:
            continue
        brief = BRIEF.format(
            offre=state["offre"], cible=a["cible"], out=os.path.abspath(out), devise=a.get("devise", "EUR"),
            unite_prix=a["unite_prix"], type_texte=TYPES[c["type"]],
            contexte_ligne=("Votre situation : %s.\n" % c["contexte"]) if c.get("contexte") else "",
            raisons=" / ".join(RAISONS), budget_txt="{:,}".format(c["budget"]).replace(",", " "), **c)
        bp = _path(d, "briefs", c["id"] + ".md")
        with open(bp, "w", encoding="utf-8") as fh:
            fh.write(brief)
        todo.append((c["id"], os.path.abspath(bp)))
    return [todo[i:i + wave] for i in range(0, len(todo), wave)]


def _reponse_ok(path, pid):
    """None si la réponse est valide, sinon un court message."""
    if not os.path.exists(path):
        return "manquante"
    try:
        a = _read_json(path)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return "JSON invalide"
    if not isinstance(a, dict):
        return "JSON invalide"
    manque = CHAMPS - set(a)
    if manque:
        return "manque " + ", ".join(sorted(manque))
    if a.get("id") != pid:
        return "id vaut %r, attendu %s" % (a.get("id"), pid)
    if not isinstance(a.get("achete"), bool):
        return "'achete' doit valoir true ou false"
    if a.get("code_raison") not in RAISONS:
        return "code_raison %r n'est pas parmi %s" % (a.get("code_raison"), ", ".join(RAISONS))
    return None


def save(d, pid, text):
    """Range la PROPRE réponse d'un acheteur qu'il a affichée au lieu de l'écrire. Jamais pour répondre à sa place."""
    _, cartes = load_state(d)
    if pid not in {c["id"] for c in cartes}:
        raise PanelError("aucun acheteur %s dans ce panel" % pid)
    start = text.find("{")
    if start < 0:
        raise PanelError("aucun objet JSON dans la réponse")
    try:
        obj, _ = json.JSONDecoder().raw_decode(text[start:])
    except json.JSONDecodeError as e:
        raise PanelError("le JSON de la réponse ne se lit pas : %s" % e)
    path = _path(d, "reponses", pid + ".json")
    _write_json(path, obj)
    prob = _reponse_ok(path, pid)
    if prob:
        os.remove(path)
        raise PanelError("la réponse de %s n'est pas valide (%s) ; relancez son brief" % (pid, prob))
    return path


def check(d):
    _, cartes = load_state(d)
    probs = []
    for c in cartes:
        p = _reponse_ok(_path(d, "reponses", c["id"] + ".json"), c["id"])
        if p:
            probs.append((c["id"], p))
    return probs


# ── décompte ───────────────────────────────────────────────────────────────────
def _taux(rows):
    return (sum(1 for r in rows if r["achete"]) / len(rows)) if rows else 0.0


def _num(v):
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def tally(d):
    state, cartes = load_state(d)
    par_id = {c["id"]: c for c in cartes}
    rows, ecartes = [], []
    for c in cartes:
        path = _path(d, "reponses", c["id"] + ".json")
        p = _reponse_ok(path, c["id"])
        if p:
            ecartes.append((c["id"], p))
            continue
        a = _read_json(path)
        rows.append(dict(par_id[c["id"]], **{k: v for k, v in a.items() if k != "id"}, id=c["id"]))
    if not rows:
        raise PanelError("aucune réponse valide : lancez d'abord les briefs (panel.py prompts)")

    def groupe(key):
        out = {}
        for r in rows:
            out.setdefault(r[key], []).append(r)
        return sorted(((k, len(v), _taux(v)) for k, v in out.items()), key=lambda t: -t[2])

    non = [r for r in rows if not r["achete"]]
    oui = [r for r in rows if r["achete"]]

    def raisons(rs):
        out = {}
        for r in rs:
            out.setdefault(r["code_raison"], []).append(r)
        return sorted(out.items(), key=lambda kv: -len(kv[1]))

    places = [_num(r.get("places")) for r in oui]
    places = [p for p in places if p is not None and p >= 0]
    return {
        "formation": state["acheteurs"]["formation"], "seed": state["seed"], "distribues": len(cartes),
        "repondu": len(rows), "ecartes": ecartes, "achats": len(oui), "refus": len(non),
        "taux_achat": len(oui) / len(rows),
        "par_type": groupe("type"), "par_segment": groupe("segment"), "par_comportement": groupe("comportement"),
        "pourquoi_non": [(k, len(v), [r["raison"] for r in v[:2]], [r["id"] for r in v[:2]]) for k, v in raisons(non)],
        "pourquoi_oui": [(k, len(v), [r["raison"] for r in v[:2]], [r["id"] for r in v[:2]]) for k, v in raisons(oui)],
        "bascule": [r["ce_qui_me_ferait_changer"] for r in non if (r.get("ce_qui_me_ferait_changer") or "").strip()],
        "places_par_acheteur": (sum(places) / len(places)) if places else None,
        "reponses_prix": sum(1 for r in rows if all(_num(r.get(k)) is not None for k in PRIX)),
    }


def resultats_md(res):
    pct = lambda v: "%.0f %%" % (v * 100)
    L = ["# Panel d'acheteurs : %s" % res["formation"], ""]
    L.append("**%d achètent · %d refusent** (%s d'achat) sur %d acheteurs simulés. Seed %s : les mêmes cartes peuvent être redistribuées."
             % (res["achats"], res["refus"], pct(res["taux_achat"]), res["repondu"], res["seed"]))
    if res["ecartes"]:
        L += ["", "%d acheteurs sur %d n'ont pas de réponse valide et sont écartés : %s." % (
            len(res["ecartes"]), res["distribues"], ", ".join("%s (%s)" % e for e in res["ecartes"][:10]))]
    L += ["", "Ce sont des acheteurs simulés, pas des clients. Servez-vous en pour trouver les objections et les points"
          " faibles, puis confirmez les plus importants avec de vrais acheteurs avant d'investir."]
    for titre, key in (("Par type d'acheteur", "par_type"), ("Par segment", "par_segment"),
                       ("Par façon d'acheter", "par_comportement")):
        L += ["", "## %s" % titre, "", "| groupe | acheteurs | taux d'achat |", "| --- | ---: | ---: |"]
        for k, n, r in res[key]:
            L.append("| %s | %d | %s%s |" % (k, n, pct(r), "  (peu de réponses)" if n < 8 else ""))
    for titre, key in (("Pourquoi ils refusent", "pourquoi_non"), ("Pourquoi ils achètent", "pourquoi_oui")):
        L += ["", "## %s" % titre, "", "| raison | acheteurs | avec leurs mots |", "| --- | ---: | --- |"]
        for k, n, quotes, ids in res[key]:
            L.append("| %s | %d | %s |" % (k, n, " · ".join("« %s » (%s)" % (q.replace("|", "/"), i) for q, i in zip(quotes, ids))))
    if res["bascule"]:
        L += ["", "## Ce qui ferait basculer un non", ""]
        for f in res["bascule"][:12]:
            L.append("- %s" % f)
    if res["places_par_acheteur"] is not None:
        L += ["", "Les acheteurs déclarent **%.1f places** la première année en moyenne." % res["places_par_acheteur"]]
    if res["reponses_prix"]:
        L += ["", "%d acheteurs ont donné les quatre réponses de prix. Lancez van_westendorp.py de formation-prix sur le dossier des réponses." % res["reponses_prix"]]
    return "\n".join(L) + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--dir", default=os.path.join("formation", "panel"))
    sub = ap.add_subparsers(dest="cmd", required=True)
    i = sub.add_parser("init")
    i.add_argument("--acheteurs", required=True)
    i.add_argument("--offre", required=True)
    i.add_argument("--n", type=int, default=100)
    i.add_argument("--seed", type=int)
    p = sub.add_parser("prompts")
    p.add_argument("--wave", type=int, default=VAGUE)
    sub.add_parser("check")
    sv = sub.add_parser("save")
    sv.add_argument("id")
    t = sub.add_parser("tally")
    t.add_argument("--out")
    sub.add_parser("status")
    a = ap.parse_args(argv)
    try:
        if a.cmd == "init":
            cartes = init(a.dir, a.acheteurs, a.offre, a.n, a.seed)
            st, _ = load_state(a.dir)
            print("%d acheteurs distribués (seed %s) dans %s. Suite : panel.py prompts" % (len(cartes), st["seed"], a.dir))
        elif a.cmd == "prompts":
            vagues = write_briefs(a.dir, a.wave)
            n = sum(len(w) for w in vagues)
            if not n:
                print("chaque acheteur a une réponse valide. Suite : panel.py tally")
            else:
                print("%d briefs en %d vagues de %d au plus. Lancez une vague à la fois :" % (n, len(vagues), a.wave))
                for k, w in enumerate(vagues, 1):
                    print("vague %d : %s" % (k, " ".join("%s=%s" % job for job in w)))
        elif a.cmd == "check":
            probs = check(a.dir)
            if not probs:
                print("toutes les réponses sont présentes et valides")
            for pid, prob in probs:
                print("%s : %s" % (pid, prob))
            return 1 if probs else 0
        elif a.cmd == "save":
            print("enregistré : %s" % save(a.dir, a.id, sys.stdin.read()))
        elif a.cmd == "tally":
            res = tally(a.dir)
            out = a.out or _path(a.dir, "resultats.md")
            with open(out, "w", encoding="utf-8") as fh:
                fh.write(resultats_md(res))
            _write_json(_path(a.dir, "resultats.json"), res)
            print("%d achètent · %d refusent (%.0f %%). Écrit : %s" % (res["achats"], res["refus"], res["taux_achat"] * 100, out))
        elif a.cmd == "status":
            st, cartes = load_state(a.dir)
            probs = check(a.dir)
            print("%d acheteurs (seed %s), %d ont répondu, %d restants" % (len(cartes), st["seed"], len(cartes) - len(probs), len(probs)))
    except PanelError as e:
        print("erreur : %s" % e, file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
