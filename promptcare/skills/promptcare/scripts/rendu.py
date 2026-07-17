#!/usr/bin/env python3
"""PromptCare — rendu HTML déterministe du rapport.

Entrée : JSON sur stdin (ou chemin en argv[1]) :
{
  "date": "15/07/2026",
  "examine": "…", "invisible": "…", "couverture": "…",
  "score": 61, "punch": "une phrase punchy",
  "problemes": [{"type": "Contradiction", "impact": "Haut", "constat": "…",
                 "extrait": "…", "etiquette": "[nouveau]"}],   # etiquette optionnelle (delta)
  "outillage": [{"outil": "…", "statut": "…", "preuve": "…",
                 "dernier_usage": "…", "reco": "…"}],           # [] si non applicable
  "top3": ["…", "…", "…"],
  "au_dela": "…",                                               # optionnel
  "pistes": "…",
  "limites": "…",
  "ecartes": [{"chemin": "…", "raison": "…"}],                  # [] si aucun
  "formules": ["Doublons : 2 × −5 = −10", …],                   # sortie de score.py
  "formule_totale": "100 − 39 = 61",                            # sortie de score.py
  "corriges": ["…"]                                             # optionnel (delta)
}
Sortie : HTML complet sur stdout (à écrire dans rapport-promptcare.html,
puis HTML → PDF). Le verdict et sa couleur sont dérivés du score : rien
n'est laissé au jugement. Aucun réseau ; lecture seule du template.
"""
import html
import json
import sys
from pathlib import Path

TEMPLATE = Path(__file__).resolve().parent.parent / "assets" / "rapport-template.html"

VERDICTS = [  # (score minimal, libellé, couleur verrouillée, variante claire du dégradé)
    (90, "réglages sains", "#1B7F4B", "#3FA36C"),
    (70, "pollution légère", "#B7791F", "#D69E2E"),
    (50, "pollution installée", "#C05621", "#DD6B20"),
    (0, "pollution sévère", "#B3261E", "#D93025"),
]

CIRCONFERENCE = 326.7  # 2π × r=52, doit rester aligné avec le template

MANIFESTE = Path(__file__).resolve().parents[3] / ".claude-plugin" / "plugin.json"


def version_plugin() -> str:
    """Version lue dans le manifeste du plugin ; vide si introuvable (jamais bloquant)."""
    try:
        return json.loads(MANIFESTE.read_text(encoding="utf-8")).get("version", "")
    except (OSError, ValueError):
        return ""


def e(v) -> str:
    return html.escape(str(v), quote=False)


def lignes_problemes(problemes: list) -> str:
    if not problemes:
        return '    <tr><td colspan="5">Aucun problème détecté.</td></tr>'
    out = []
    for i, p in enumerate(problemes, 1):
        etq = f'<span class="etq">{e(p["etiquette"])}</span> ' if p.get("etiquette") else ""
        impact = e(p.get("impact", ""))
        out.append(
            f'    <tr><td>{i}</td><td>{e(p.get("type", ""))}</td>'
            f'<td class="impact-{impact}">{impact}</td>'
            f'<td>{etq}{e(p.get("constat", ""))}</td>'
            f'<td>{e(p.get("extrait", "—")) or "—"}</td></tr>'
        )
    return "\n".join(out)


def bloc_outillage(outillage: list) -> str:
    if not outillage:
        return ""
    lignes = "\n".join(
        f'    <tr><td>{e(o.get("outil", ""))}</td><td>{e(o.get("statut", ""))}</td>'
        f'<td>{e(o.get("preuve", "—")) or "—"}</td><td>{e(o.get("dernier_usage", "—")) or "—"}</td>'
        f'<td>{e(o.get("reco", ""))}</td></tr>'
        for o in outillage
    )
    return (
        '<div class="carte">\n<h2>🧰 Outillage</h2>\n<table>\n'
        "  <thead><tr><th>Outil</th><th>Statut</th><th>Preuve</th>"
        "<th>Dernier usage constaté</th><th>Recommandation</th></tr></thead>\n"
        f"  <tbody>\n{lignes}\n  </tbody>\n</table>\n</div>"
    )


def bloc_corriges(corriges: list) -> str:
    if not corriges:
        return ""
    items = " · ".join(e(c) for c in corriges)
    return f'<div class="carte corriges"><b>✅ Corrigé depuis le dernier audit :</b> {items}</div>'


def rendre(d: dict) -> str:
    score = int(d["score"])
    if not 0 <= score <= 100:
        raise ValueError(f"score {score} hors de [0, 100]")
    libelle, couleur, couleur_claire = next(
        (lib, coul, clair) for mini, lib, coul, clair in VERDICTS if score >= mini
    )

    gabarit = TEMPLATE.read_text(encoding="utf-8")
    formules = d.get("formules", [])
    lignes_detail = "\n".join(f"  <div>{e(f)}</div>" for f in formules) or "  <div>Aucune pénalité.</div>"
    au_dela = f'<div class="audela">{e(d["au_dela"])}</div>' if d.get("au_dela") else ""
    ecartes = d.get("ecartes", [])
    ecartes_txt = " · ".join(f'{e(x["chemin"])} — {e(x["raison"])}' for x in ecartes) or "Aucun."

    remplacements = {
        "{{DATE}}": e(d.get("date", "")),
        "{{VERSION}}": f" · PromptCare v{e(version_plugin())}" if version_plugin() else "",
        "{{EXAMINE}}": e(d.get("examine", "")),
        "{{INVISIBLE}}": e(d.get("invisible", "")),
        "{{COUVERTURE}}": e(d.get("couverture", "")),
        "{{SCORE}}": str(score),
        "{{VERDICT}}": e(libelle),
        "{{COULEUR_VERDICT}}": couleur,
        "{{COULEUR_VERDICT_CLAIRE}}": couleur_claire,
        "{{DASH}}": f"{score / 100 * CIRCONFERENCE:.1f}",
        "{{PUNCH}}": e(d.get("punch", "")),
        "{{BLOC_CORRIGES}}": bloc_corriges(d.get("corriges", [])),
        "{{LIGNES_PROBLEMES}}": lignes_problemes(d.get("problemes", [])),
        "{{BLOC_OUTILLAGE}}": bloc_outillage(d.get("outillage", [])),
        "{{LIGNES_TOP3}}": "\n".join(f"  <li>{e(t)}</li>" for t in d.get("top3", [])),
        "{{AU_DELA}}": au_dela,
        "{{PISTES}}": e(d.get("pistes", "")),
        "{{LIMITES}}": e(d.get("limites", "")),
        "{{ECARTES}}": ecartes_txt,
        "{{LIGNES_DETAIL}}": lignes_detail,
        "{{FORMULE_TOTALE}}": e(d.get("formule_totale", "")),
    }
    for cle, valeur in remplacements.items():
        gabarit = gabarit.replace(cle, valeur)
    if "{{" in gabarit:
        reste = sorted({m.split("}}")[0] + "}}" for m in gabarit.split("{{")[1:]})
        raise ValueError(f"placeholders non remplis : {', '.join(reste)}")
    return gabarit


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    try:
        if len(sys.argv) > 1:
            with open(sys.argv[1], "r", encoding="utf-8") as fh:
                data = json.load(fh)
        else:
            data = json.load(sys.stdin)
        print(rendre(data))
    except (KeyError, ValueError, OSError, json.JSONDecodeError) as exc:
        print(json.dumps({"erreur": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
