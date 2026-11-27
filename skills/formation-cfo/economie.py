#!/usr/bin/env python3
"""Économie d'une formation, pour formation-cfo. Bibliothèque standard uniquement, aucun accès réseau.

Lit un fichier JSON qui décrit la formation et calcule ce qu'un directeur financier
vérifierait avant de lancer la première session : ce que rapporte une session, le
nombre de participants à partir duquel elle couvre ses coûts, ce que vous gagnez
réellement par jour de travail (préparation et conception comprises), le résultat
de l'année 1 et ce qui se passe si le prix, le remplissage ou le nombre de sessions
baisse.

    python3 economie.py formation/chiffres.json
    python3 economie.py formation/chiffres.json --out formation/cfo.md
    python3 economie.py formation/chiffres.json --json
    python3 economie.py formation/chiffres.json --prix 0.9 --remplissage 0.7 --sessions 0.5

Le fichier d'entrée (voir exemple.json dans ce dossier) :

    formation              nom, pour le rapport
    devise                 "EUR" par défaut
    taux_journalier_cible  ce que le formateur veut gagner par jour mobilisé (facultatif)
    jours_conception       jours de conception à investir une seule fois (facultatif)
    lancement              [{label, cout}] dépenses uniques avant la première session
    fixes_annuels          [{label, cout}] coûts annuels quel que soit le nombre de sessions
    formats                une entrée par façon de vendre la formation :
        nom                    "Inter-entreprises", "Intra", "En ligne", "Sous-traitance"...
        mode                   "participant" (prix par participant) ou "session" (prix par session)
        prix                   hors taxes
        duree_jours            durée d'animation d'une session, en jours
        participants_prevus    participants attendus par session
        capacite               participants maximum par session (facultatif)
        sessions_annee_1       nombre de sessions prévues l'année 1
        commission_pct         part prélevée par un intermédiaire (organisme, plateforme), en %
        jours_prep_par_session préparation, déplacement, suivi par session, en jours
        couts_par_participant  [{label, cout}] supports, repas, certificat...
        couts_par_session      [{label, cout}] salle, déplacement, matériel, co-animation...

Chaque nombre du rapport vient de ce fichier. Rien n'est cherché ni deviné. S'il
manque un champ, l'outil le dit au lieu de le remplir.

Les options --prix, --remplissage et --sessions appliquent un coefficient à tous
les formats, sans modifier le fichier (0.9 = 10 % de moins).

Pensé pour formation-cfo du pack formateur, sur le modèle de unit_economics.py de
founder-skill (Jake Schincariol, licence MIT).
"""

import argparse
import copy
import json
import math
import sys


class ChiffresError(Exception):
    pass


def _nb(v, champ):
    try:
        return float(v)
    except (TypeError, ValueError):
        raise ChiffresError("%s n'est pas un nombre : %r" % (champ, v))


def _somme(items, champ):
    total = 0.0
    for i, it in enumerate(items or []):
        if not isinstance(it, dict) or "cout" not in it:
            raise ChiffresError("%s[%d] doit avoir un 'cout'" % (champ, i))
        total += _nb(it["cout"], "%s[%d].cout" % (champ, i))
    return total


def argent(v, devise="EUR"):
    signe = "-" if v < 0 else ""
    return "%s%s %s" % (signe, "{:,.0f}".format(abs(round(v))).replace(",", " "), devise)


def _g(v):
    return ("%g" % round(v, 2)).replace(".", ",")


def charger(path):
    try:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    except FileNotFoundError:
        raise ChiffresError("fichier introuvable : %s" % path)
    except json.JSONDecodeError as e:
        raise ChiffresError("%s n'est pas un JSON valide : %s" % (path, e))


def _format(f, i, taux):
    nom = f.get("nom") or "format %d" % (i + 1)
    for k in ("mode", "prix", "duree_jours", "participants_prevus", "sessions_annee_1"):
        if k not in f:
            raise ChiffresError("le format %r doit avoir '%s'" % (nom, k))
    mode = f["mode"]
    if mode not in ("participant", "session"):
        raise ChiffresError("le mode du format %r doit être 'participant' ou 'session'" % nom)
    prix = _nb(f["prix"], nom + ".prix")
    if prix <= 0:
        raise ChiffresError("le prix du format %r doit être supérieur à zéro" % nom)
    part = _nb(f["participants_prevus"], nom + ".participants_prevus")
    duree = _nb(f["duree_jours"], nom + ".duree_jours")
    prep = _nb(f.get("jours_prep_par_session", 0), nom + ".jours_prep_par_session")
    sessions = _nb(f["sessions_annee_1"], nom + ".sessions_annee_1")
    comm = _nb(f.get("commission_pct", 0), nom + ".commission_pct") / 100.0
    if not 0 <= comm < 1:
        raise ChiffresError("commission_pct du format %r doit être entre 0 et 100 (exclu)" % nom)
    cap = f.get("capacite")
    cap = None if cap is None else _nb(cap, nom + ".capacite")
    c_part = _somme(f.get("couts_par_participant"), nom + ".couts_par_participant")
    c_sess = _somme(f.get("couts_par_session"), nom + ".couts_par_session")
    jours = duree + prep
    if jours <= 0:
        raise ChiffresError("le format %r doit mobiliser plus de zéro jour" % nom)

    ca = prix * part if mode == "participant" else prix
    commission = ca * comm
    variables = c_part * part + c_sess
    contribution = ca - commission - variables

    # seuils (nombre de participants) : seulement quand le revenu dépend des participants
    seuil = seuil_taux = None
    if mode == "participant":
        marge_part = prix * (1 - comm) - c_part
        seuil = math.inf if marge_part <= 0 else max(1, math.ceil(c_sess / marge_part - 1e-9))
        if taux:
            seuil_taux = math.inf if marge_part <= 0 else max(1, math.ceil((c_sess + taux * jours) / marge_part - 1e-9))
    alertes = []
    if contribution <= 0:
        alertes.append("%s : une session au remplissage prévu perd de l'argent (%s)." % (nom, argent(contribution)))
    if cap is not None and part > cap:
        alertes.append("%s : %s participants prévus pour une capacité de %s." % (nom, _g(part), _g(cap)))
    if taux and contribution > 0 and contribution / jours < taux:
        alertes.append("%s : une session rapporte %s par jour mobilisé, sous votre cible de %s." % (
            nom, argent(contribution / jours), argent(taux)))
    if seuil is not None and cap is not None and seuil > cap:
        alertes.append("%s : il faut %s participants pour couvrir les coûts d'une session, au-delà de la capacité (%s)." % (
            nom, "une infinité de" if math.isinf(seuil) else "%d" % seuil, _g(cap)))
    return {
        "nom": nom, "mode": mode, "prix": prix, "participants": part, "capacite": cap, "sessions": sessions,
        "duree_jours": duree, "prep_jours": prep, "jours_par_session": jours, "commission_pct": comm * 100,
        "ca_session": ca, "commission_session": commission, "variables_session": variables,
        "contribution_session": contribution, "par_jour": contribution / jours,
        "seuil_participants": seuil, "seuil_participants_taux": seuil_taux,
        "ca_annee": ca * sessions, "contribution_annee": contribution * sessions, "jours_annee": jours * sessions,
        "couts_par_participant": f.get("couts_par_participant", []), "couts_par_session": f.get("couts_par_session", []),
        "alertes": alertes,
    }


def analyser(spec, prix=1.0, remplissage=1.0, sessions=1.0):
    """Renvoie un dict avec chaque nombre du rapport. Fonction pure, facile à tester."""
    formats = spec.get("formats")
    if not formats:
        raise ChiffresError("'formats' est vide : décrivez au moins une façon de vendre la formation")
    s = copy.deepcopy(spec)
    for f in s["formats"]:
        if "prix" in f:
            f["prix"] = _nb(f["prix"], "prix") * prix
        if "participants_prevus" in f:
            f["participants_prevus"] = _nb(f["participants_prevus"], "participants_prevus") * remplissage
        if "sessions_annee_1" in f:
            f["sessions_annee_1"] = _nb(f["sessions_annee_1"], "sessions_annee_1") * sessions
    taux = s.get("taux_journalier_cible")
    taux = None if taux in (None, "", 0) else _nb(taux, "taux_journalier_cible")
    fs = [_format(f, i, taux) for i, f in enumerate(s["formats"])]
    fixes = _somme(s.get("fixes_annuels"), "fixes_annuels")
    lancement = _somme(s.get("lancement"), "lancement")
    conception = _nb(s.get("jours_conception", 0), "jours_conception")

    contribution = sum(f["contribution_annee"] for f in fs)
    ca = sum(f["ca_annee"] for f in fs)
    jours_sessions = sum(f["jours_annee"] for f in fs)
    jours_total = jours_sessions + conception
    resultat = contribution - fixes - lancement
    par_jour = resultat / jours_total if jours_total else None
    nb_sessions = sum(f["sessions"] for f in fs)
    contrib_moy = contribution / nb_sessions if nb_sessions else 0
    sessions_equilibre = math.inf if contrib_moy <= 0 else (fixes + lancement) / contrib_moy

    alertes = [a for f in fs for a in f["alertes"]]
    if resultat < 0:
        alertes.append("L'année 1 perd de l'argent après coûts fixes et lancement (%s)." % argent(resultat, s.get("devise", "EUR")))
    if taux and par_jour is not None and par_jour < taux:
        alertes.append("Sur l'année 1, conception comprise, vous gagnez %s par jour mobilisé, sous votre cible de %s." % (
            argent(par_jour, s.get("devise", "EUR")), argent(taux, s.get("devise", "EUR"))))
    return {
        "formation": s.get("formation", ""), "devise": s.get("devise", "EUR"), "taux_cible": taux,
        "formats": fs, "fixes_annuels": fixes, "lancement": lancement, "jours_conception": conception,
        "ca_annee": ca, "contribution_annee": contribution, "resultat_annee": resultat,
        "jours_sessions": jours_sessions, "jours_total": jours_total, "par_jour_annee": par_jour,
        "sessions_annee": nb_sessions, "sessions_equilibre": sessions_equilibre, "alertes": alertes,
        "fixes_items": s.get("fixes_annuels", []), "lancement_items": s.get("lancement", []),
    }


def sensibilite(spec):
    """Les trois scénarios qu'un plan de formation doit encaisser."""
    return [("Plan de base", analyser(spec)),
            ("Prix -10 %", analyser(spec, prix=0.9)),
            ("Remplissage -30 %", analyser(spec, remplissage=0.7)),
            ("Moitié des sessions", analyser(spec, sessions=0.5))]


def _seuil(v):
    if v is None:
        return "sans objet (prix par session)"
    return "jamais" if math.isinf(v) else "%d" % v


def rapport(spec, a):
    d = a["devise"]
    m = lambda v: argent(v, d)
    L = ["# Économie de la formation : %s" % (a["formation"] or "votre formation"), "",
         "Chaque nombre ci-dessous vient du fichier d'entrée. Rien n'est cherché ni deviné. Montants hors taxes.", ""]
    L += ["## Une session, format par format", "",
          "| | " + " | ".join(f["nom"] for f in a["formats"]) + " |",
          "| --- |" + " ---: |" * len(a["formats"])]
    rows = [
        ("Prix", lambda f: "%s %s" % (m(f["prix"]), "par participant" if f["mode"] == "participant" else "par session")),
        ("Participants prévus", lambda f: "%s%s" % (_g(f["participants"]), "" if f["capacite"] is None else " (max %s)" % _g(f["capacite"]))),
        ("Chiffre d'affaires", lambda f: m(f["ca_session"])),
        ("Commission intermédiaire", lambda f: "-" + m(f["commission_session"]) if f["commission_session"] else m(0)),
        ("Coûts directs", lambda f: "-" + m(f["variables_session"])),
        ("**Ce qui reste**", lambda f: "**%s**" % m(f["contribution_session"])),
        ("Jours mobilisés (animation + préparation)", lambda f: _g(f["jours_par_session"])),
        ("**Gagné par jour mobilisé**", lambda f: "**%s**" % m(f["par_jour"])),
        ("Seuil : participants pour couvrir les coûts", lambda f: _seuil(f["seuil_participants"])),
    ]
    if a["taux_cible"]:
        rows.append(("Participants pour atteindre %s par jour" % m(a["taux_cible"]), lambda f: _seuil(f["seuil_participants_taux"])))
    for lab, fn in rows:
        L.append("| %s | %s |" % (lab, " | ".join(fn(f) for f in a["formats"])))
    L += ["", "Détail des coûts directs :", ""]
    for f in a["formats"]:
        items = ["%s %s par participant" % (it.get("label", "coût"), m(float(it["cout"]))) for it in f["couts_par_participant"]]
        items += ["%s %s par session" % (it.get("label", "coût"), m(float(it["cout"]))) for it in f["couts_par_session"]]
        L.append("- %s : %s." % (f["nom"], ", ".join(items) if items else "aucun coût direct renseigné"))
    L += ["", "## L'année 1", "",
          "| format | sessions | chiffre d'affaires | ce qui reste | jours |", "| --- | ---: | ---: | ---: | ---: |"]
    for f in a["formats"]:
        L.append("| %s | %s | %s | %s | %s |" % (f["nom"], _g(f["sessions"]), m(f["ca_annee"]), m(f["contribution_annee"]), _g(f["jours_annee"])))
    L += ["", "- Chiffre d'affaires : **%s**." % m(a["ca_annee"]),
          "- Coûts fixes annuels : %s (%s)." % (m(a["fixes_annuels"]), ", ".join(
              "%s %s" % (it.get("label", "coût"), m(float(it["cout"]))) for it in a["fixes_items"]) or "aucun renseigné"),
          "- Dépenses de lancement : %s (%s)." % (m(a["lancement"]), ", ".join(
              "%s %s" % (it.get("label", "coût"), m(float(it["cout"]))) for it in a["lancement_items"]) or "aucune renseignée"),
          "- **Résultat de l'année 1 : %s**, après coûts fixes et lancement." % m(a["resultat_annee"]),
          "- Jours mobilisés : %s (sessions %s + conception %s)." % (_g(a["jours_total"]), _g(a["jours_sessions"]), _g(a["jours_conception"]))]
    if a["par_jour_annee"] is not None:
        L.append("- **Gagné par jour mobilisé sur l'année, conception comprise : %s**%s." % (
            m(a["par_jour_annee"]), "" if not a["taux_cible"] else " (cible : %s)" % m(a["taux_cible"])))
    se = a["sessions_equilibre"]
    L.append("- Sessions nécessaires pour couvrir coûts fixes et lancement, au rythme prévu : %s." % (
        "jamais (une session moyenne ne rapporte rien)" if math.isinf(se) else _g(round(se, 1))))
    L += ["", "## Et si", "", "| scénario | résultat année 1 | gagné par jour mobilisé |", "| --- | ---: | ---: |"]
    for nom, s in sensibilite(spec):
        L.append("| %s | %s | %s |" % (nom, m(s["resultat_annee"]), "n/d" if s["par_jour_annee"] is None else m(s["par_jour_annee"])))
    L.append("")
    if a["alertes"]:
        L += ["## Signaux d'alerte", ""] + ["- %s" % x for x in a["alertes"]]
    else:
        L.append("Aucun signal d'alerte dans ces chiffres. Ils ne valent que ce que valent les entrées : vérifiez chaque coût sur un vrai devis.")
    return "\n".join(L) + "\n"


def _json_safe(o):
    if isinstance(o, float) and math.isinf(o):
        return None
    if isinstance(o, dict):
        return {k: _json_safe(v) for k, v in o.items()}
    if isinstance(o, list):
        return [_json_safe(v) for v in o]
    return o


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("chiffres", help="le fichier chiffres.json de la formation")
    ap.add_argument("--out", help="écrire le rapport ici (markdown)")
    ap.add_argument("--json", action="store_true", help="afficher les nombres en JSON")
    ap.add_argument("--prix", type=float, default=1.0, help="coefficient sur les prix (0.9 = -10 %%)")
    ap.add_argument("--remplissage", type=float, default=1.0, help="coefficient sur les participants")
    ap.add_argument("--sessions", type=float, default=1.0, help="coefficient sur le nombre de sessions")
    a = ap.parse_args(argv)
    try:
        spec = charger(a.chiffres)
        res = analyser(spec, a.prix, a.remplissage, a.sessions)
        if (a.prix, a.remplissage, a.sessions) != (1.0, 1.0, 1.0):
            spec = copy.deepcopy(spec)
            for f in spec["formats"]:
                f["prix"] = float(f["prix"]) * a.prix
                f["participants_prevus"] = float(f["participants_prevus"]) * a.remplissage
                f["sessions_annee_1"] = float(f["sessions_annee_1"]) * a.sessions
    except ChiffresError as e:
        print("erreur : %s" % e, file=sys.stderr)
        return 2
    if a.json:
        out = {k: v for k, v in res.items() if not k.endswith("_items")}
        print(json.dumps(_json_safe(out), indent=1, ensure_ascii=False))
        return 0
    text = rapport(spec, res)
    if a.out:
        with open(a.out, "w", encoding="utf-8") as fh:
            fh.write(text)
        print("écrit : %s" % a.out)
    else:
        sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
