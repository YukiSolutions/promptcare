#!/usr/bin/env python3
"""PromptCare — calcul déterministe du score de santé.

Entrée : JSON sur stdin (ou chemin de fichier en argv[1]) au schéma :
{
  "findings": [
    {"axe": "contradiction", "gravite": "majeure"},   # gravite requise pour cet axe
    {"axe": "doublon"},
    {"axe": "obsolete"},
    {"axe": "bruit"},
    {"axe": "trou"},
    {"axe": "risque"},
    {"axe": "outillage"}
  ]
}
Sortie : JSON (score, verdict, détail par axe, ligne prête pour le rapport).
Aucun réseau, aucune écriture : fonction pure.
"""
import json
import sys

# Barème verrouillé — pénalité unitaire et plafond par axe.
BAREME = {
    "contradiction": {"penalites": {"majeure": 15, "mineure": 5}, "plafond": 25},
    "doublon":   {"penalites": {None: 5}, "plafond": 15},
    "obsolete":  {"penalites": {None: 5}, "plafond": 15},
    "bruit":     {"penalites": {None: 2}, "plafond": 10},
    "trou":      {"penalites": {None: 3}, "plafond": 10},
    "risque":    {"penalites": {None: 8}, "plafond": 15},
    "outillage": {"penalites": {None: 2}, "plafond": 10},
}

LIBELLES = {
    "contradiction": "Contradictions", "doublon": "Doublons", "obsolete": "Obsolète",
    "bruit": "Bruit", "trou": "Trous", "risque": "Risques", "outillage": "Outillage",
}


def verdict(score: int) -> str:
    if score >= 90:
        return "réglages sains"
    if score >= 70:
        return "pollution légère"
    if score >= 50:
        return "pollution installée"
    return "pollution sévère"


def calculer(findings: list) -> dict:
    bruts = {axe: 0 for axe in BAREME}
    comptes = {axe: 0 for axe in BAREME}
    par_gravite = {axe: {} for axe in BAREME}

    for i, f in enumerate(findings):
        axe = f.get("axe")
        if axe not in BAREME:
            raise ValueError(f"finding {i}: axe inconnu '{axe}' (attendus: {', '.join(BAREME)})")
        gravite = f.get("gravite")
        penalites = BAREME[axe]["penalites"]
        if None in penalites:
            pen = penalites[None]
            gravite = None
        else:
            if gravite not in penalites:
                raise ValueError(
                    f"finding {i}: axe '{axe}' exige une gravite parmi {sorted(k for k in penalites)}"
                )
            pen = penalites[gravite]
        bruts[axe] += pen
        comptes[axe] += 1
        par_gravite[axe][gravite] = par_gravite[axe].get(gravite, 0) + 1

    detail = {}
    formules = []
    total = 0
    for axe, brut in bruts.items():
        plafond = BAREME[axe]["plafond"]
        applique = min(brut, plafond)
        if applique:
            detail[axe] = {
                "constats": comptes[axe],
                "penalite_brute": brut,
                "penalite": applique,
                "plafonne": brut > plafond,
            }
            pens = BAREME[axe]["penalites"]
            termes = [
                f"{n} × −{pens[g]}" + (f" ({g})" if g else "")
                for g, n in sorted(par_gravite[axe].items(), key=lambda kv: -pens[kv[0]])
            ]
            calcul = " + ".join(termes) + f" = −{brut}"
            if brut > plafond:
                calcul += f", plafonné à −{plafond}"
            formules.append(f"{LIBELLES[axe]} : {calcul}")
        total += applique

    score = max(0, 100 - total)

    morceaux = [
        f"{LIBELLES[a]} −{d['penalite']}" + (" (cap)" if d["plafonne"] else "")
        for a, d in detail.items()
    ]
    ligne = " · ".join(morceaux) + f" = −{total} → {score}/100" if morceaux else f"aucune pénalité → {score}/100"
    formule_totale = f"100 − {total} = {score}" if total else "100 − 0 = 100"
    if 100 - total < 0:
        formule_totale = f"100 − {total} = {100 - total}, plancher 0 → {score}"

    return {"score": score, "verdict": verdict(score), "penalite_totale": total,
            "detail": detail, "formules": formules, "formule_totale": formule_totale,
            "ligne_rapport": ligne}


def main() -> int:
    # Console Windows en cp1252 : le « − » (U+2212) de la ligne rapport ferait
    # planter print — on force la sortie en UTF-8 quand c'est possible.
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    try:
        if len(sys.argv) > 1:
            with open(sys.argv[1], "r", encoding="utf-8") as fh:
                data = json.load(fh)
        else:
            data = json.load(sys.stdin)
        findings = data["findings"]
        if not isinstance(findings, list):
            raise ValueError('"findings" doit être une liste')
        resultat = calculer(findings)
    except (KeyError, ValueError, json.JSONDecodeError) as exc:
        print(json.dumps({"erreur": str(exc)}, ensure_ascii=False))
        return 1
    print(json.dumps(resultat, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
