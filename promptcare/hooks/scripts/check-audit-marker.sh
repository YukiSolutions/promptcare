#!/usr/bin/env bash
# PromptCare — veille passive.
# Si un marqueur d'audit existe dans le dossier courant et date de plus de 30 jours,
# suggère un audit delta. Ne fait rien d'autre : aucune écriture, aucun réseau.

set -u
MARKER="PROMPTCARE-AUDIT.md"

[ -f "$MARKER" ] || exit 0

now=$(date +%s)
# stat GNU (Linux) puis BSD (macOS)
mod=$(stat -c %Y "$MARKER" 2>/dev/null || stat -f %m "$MARKER" 2>/dev/null) || exit 0

age_days=$(( (now - mod) / 86400 ))

if [ "$age_days" -ge 30 ]; then
  echo "🩺 PromptCare : ton dernier audit (${MARKER}) date de ${age_days} jours. Lance /promptcare — je comparerai avec ce résultat et je te dirai seulement ce qui a changé depuis."
fi

exit 0
