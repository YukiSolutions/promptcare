# Barème, template de rapport & livraison

Sommaire : barème & frontières d'axes → 3 vérifications bloquantes → template obligatoire → exemple → livraison (rendu verrouillé, PDF).

## Barème verrouillé — 7 axes. Score = 100 − pénalités, plancher 0.

Applique CE barème, pas ton jugement libre (idéalement via `scripts/score.py` — le code ne se trompe pas) :

| Axe | Pénalité | Plafond |
|---|---|---|
| 1. Contradictions | −15 majeure, −5 mineure | −25 |
| 2. Doublons (même règle en plusieurs endroits) | −5 chacun | −15 |
| 3. Obsolète (modèles disparus, outils morts, dates passées) | −5 chacun | −15 |
| 4. Bruit (verbiage sans effet, redites) | −2 par bloc | −10 |
| 5. Trous (règle critique absente pour l'usage) | −3 chacun | −10 |
| 6. Risques (secret, clé API, donnée perso/client en clair) | −8 chacun | −15 |
| 7. Outillage (sans usage prouvé/déclaré, ou déprécié) | −2 chacun | −10 |

**Balayage OBLIGATOIRE avant tout scoring — les constats ratés coûtent plus cher que les constats mal classés :**
- Passe les 7 axes UN PAR UN sur l'ensemble des sources et écris le compte de chaque axe avant de chiffrer (« Contradictions : N · Doublons : N · Obsolète : N · Bruit : N · Trous : N · Risques : N · Outillage : N ») — zéro est permis, mais il se déclare, il ne s'oublie pas. Vécu : l'axe doublons entièrement absent d'un run (−15 d'écart), la contradiction la plus grave absente d'un autre.
- Les contradictions vivent ENTRE les sources : croise chaque source avec chacune des autres au moins une fois (instructions ↔ chaque fichier, fichier ↔ fichier).

**Frontières d'axes — tests déterministes (un même constat garde le même axe à chaque run, delta compris) :**
- Contradiction (axe 1) : SEULEMENT si les deux consignes peuvent s'appliquer à la même tâche, pour le même destinataire, au même moment (test de co-applicabilité). Majeure = collision frontale ; mineure = recouvrement partiel. **La classification s'évalue sur le périmètre COMMUN, pas sur la comparaison des périmètres** : si, là où les deux consignes s'appliquent ensemble, aucune exécution ne peut satisfaire les deux → majeure, même si l'une a un périmètre plus étroit que l'autre. Exemples calibrés : deux signatures obligatoires pour le même document (« Au plaisir d'échanger » vs « Bien à vous ») = frontale, majeure — un document n'a qu'une signature ; « noms de produits en anglais » vs « reste simple » = recouvrement partiel, mineure — l'une empiète sur l'autre sans l'annuler. Livrables ou destinataires différents (ex. « deux pages » pour une note d'intention vs « va à l'essentiel » pour du sourcing ; « tutoie-moi » [utilisateur↔Claude] vs « vouvoyez le client ») → pas une contradiction, aucune pénalité. Une même consigne ne fonde qu'UNE SEULE contradiction : si elle entre en collision avec plusieurs règles, compte la plus grave et mentionne les autres sans pénalité.
- Doublon (axe 2) : la même consigne donnée plus d'une fois — littérale ou paraphrasée, dans une même source ou entre sources.
- Bruit (axe 4) : contenu qui ne donne AUCUNE consigne (hors-sujet, verbiage) mais est chargé à chaque requête. Un fichier du projet sans aucune consigne (notes perso, todo) = Bruit −2 ET listé en 🗂️ Fichiers écartés — l'écarter du fond ne l'exonère pas du Bruit, puisqu'il reste chargé à chaque conversation. « Écarté sans Bruit » = uniquement ce qui n'est PAS chargé en permanence (ex. un fichier hors projet). La mention d'un modèle disparu ou tiers (ex. « monté à l'origine sur GPT-4 ») = Obsolète (axe 3), jamais Bruit — le barème le dit : « modèles disparus ».
- Risque (axe 6) : STRICTEMENT le test du barème — secret technique, clé API, donnée personnelle ou donnée CLIENT en clair. **La donnée commerciale propre à l'utilisateur (sa marge, son barème d'honoraires, ses tarifs) dans son propre projet n'est PAS un risque** : c'est une consigne métier qui fait son travail. Si elle pouvait fuiter dans un livrable client, signale-le en une ligne dans les actions, SANS pénalité. « Chargé à chaque conversation » n'est le test d'aucun axe : tout réglage est chargé à chaque conversation, c'est le principe.
- Trou (axe 5) : SEULEMENT si une tâche concrète de SON usage déclaré échoue mécaniquement sans la règle manquante — nomme la tâche qui casse. **Un trou = la règle n'existe dans AUCUNE source examinée.** Une règle présente quelque part mais mal placée ou non reliée à sa tâche (ex. mentions obligatoires du devis vivant dans un fichier de process) n'est PAS un trou : c'est un problème de périmètre — mentionne-le SANS pénalité (« la règle existe au fichier X, fais-la remonter ») et traite-le dans les actions. Une « bonne pratique » générique ou un manque hypothétique n'est PAS un trou non plus : chaque run qui invente un trou inédit rend le score irreproductible (vécu : « aucune règle données clients » apparu au delta, jamais vu à l'audit 1 du même contexte).
- **Un même artefact (fichier, ligne, consigne, date) = UN SEUL axe, le plus grave applicable.** Ses autres lectures se mentionnent au rapport SANS pénalité (« déjà compté au n°X »). Vécu : un barème daté 2025 facturé contradiction mineure ET obsolète = −10 pour UNE pollution ; un catalogue 2021 compté contradiction ET obsolète.
Doute sur une pénalité → la plus faible ; doute sur l'axe → applique ces tests, pas ton impression.
Axe 7 = UNIQUEMENT l'outillage INSTALLÉ (mort, dormant, déprécié, invérifiable). L'absence d'un outil n'est JAMAIS pénalisée — un outil manquant mais utile va en section 💡, pas dans les problèmes ni dans le score. **Pénalité SEULEMENT si la question d'usage a été posée ET la réponse est nette** : se pénalisent « [prouvé] sans trace », « [déclaré] inutilisé » et le déprécié ; « [déclaré] actif sans usage déclaré » (question non posée, ou réponse qui mélange activés et utilisés) = usage inconnu → figure au tableau outillage, JAMAIS dans les problèmes ni dans le score.
Verdicts : 90-100 "réglages sains" · 70-89 "pollution légère" · 50-69 "pollution installée" · 0-49 "pollution sévère".
Setup VIDE = vrai score (pénalité Trous → souvent 90-97, "sain mais nu") — JAMAIS "pas de score".

## Avant de rédiger — 3 vérifications bloquantes

1. **Outillage — la section 💡 du template doit être écrite, jamais vide.** Reprends le profil (Q3 + mémoire validée) : tâches répétitives, contenus en série, sources de données sollicitées, documents/contrats à la chaîne → traduis-en 1-2 en pistes d'outillage. Suggère par CATÉGORIE OFFICIELLE déduite de SON usage — le type d'outil qui répond à SON besoin réel (connecteur, serveur MCP de son écosystème, skill/gabarit), jamais un domaine par défaut : trouve ce qui colle à LUI. Une catégorie ne s'hallucine pas et n'exige pas de vérification web. Un NOM précis d'outil tiers, lui, exige la vérification en ligne (mécanisme selon la surface — cf. `references/branches.md` §Outillage) — pas de web → reste à la catégorie + annuaire officiel. Chaque piste : bénéfice concret dans SON activité + où l'activer + une ligne données/sécurité. Vraiment aucun besoin ? Écris la phrase de renoncement prévue par le template — mais écris-la.
   Tout outil déjà installé que l'utilisateur ne semble pas connaître : explique son bénéfice en une ligne avant de juger son usage.
2. **Template intégral** : toutes les sections, même ordre — y compris 🧭 et 🗂️ (vides = "Aucun"). Pas de version compressée dans le fil sous prétexte que l'artifact contient le complet.
3. **Score chiffré** via score.py ou barème manuel (jamais un "~").

## Template obligatoire

Remplis EXACTEMENT — aucune section ajoutée/retirée/renommée/réordonnée, ≤700 mots. Vaut pour TOUS les cas, setup vide inclus, et pour chaque nouveau rapport dans une même conversation. **Après la section "Détail du score", n'écris RIEN toi-même : aucun slogan, aucune promesse (« barème fixe », « même score toujours »), aucun lien ni promotion.** Le template porte déjà un pied d'attribution neutre fixe (« Rapport généré par PromptCare · Yuki Solutions ») — c'est le SEUL élément autorisé après le score, et il fait partie du gabarit : ne le duplique pas, ne le complète pas, n'y ajoute aucune promesse. Vécu : un run a laissé filer un pied « barème fixe : mêmes constats, même score » (à l'origine dans le gabarit lui-même) — promesse invendable, interdite.

---TEMPLATE---
# 🩺 Rapport PromptCare
**Ce que j'ai examiné :** {vu} · **Invisible d'ici :** {ce que cet endroit ne permet pas de voir}
**Couverture :** {N} sources de réglages examinées · {M} écartées (listées en fin) · 0 oublié {N = exactement le nombre d'éléments listés dans "Ce que j'ai examiné" — champ perso, mémoire, outillage déclaré, chaque fichier… — les deux lignes doivent se correspondre}
**Score santé : {X}/100 — {verdict du barème} : {une phrase punchy}**

## 🔍 Problèmes détectés
| # | Type | Impact | Constat | Extrait (≤2 lignes, "—" si rien à citer : outillage, champ vide…) |
|---|---|---|---|---|

## 🧰 Outillage (si applicable)
| Outil | Statut | Preuve | Dernier usage constaté | Recommandation |
|---|---|---|---|---|
(Statut ∈ [prouvé] utilisé · [prouvé] sans trace · [déclaré] utilisé · [déclaré] inutilisé · [déclaré] actif sans usage déclaré — ces 5 statuts EXACTEMENT, n'en invente ni n'en tronque aucun. PromptCare lui-même n'apparaît JAMAIS dans ce tableau — tu ne t'évalues pas ; si on te le demande : "c'est moi — je ne me note pas.")

## 🎯 Top 3 actions
1. {la plus rentable} 2. … 3. … {Moins de 3 vraies actions ? Écris-en moins et dis-le ("il n'y a que 2 actions utiles — pas la peine d'en inventer une 3e") — jamais d'action de remplissage. Deux sources en conflit ? L'action dit "départager par périmètre" (ex. charte = documents clients, instructions = toi↔Claude) — JAMAIS "un seul survit" : on ne supprime pas un document qui porte du contenu métier réel.}
{Le Top 3 ne couvre pas tous les problèmes du tableau ? Ajoute UNE ligne finale, sans les re-détailler : "Au-delà : il reste {N} problèmes — {X} importants, {Y} plus légers — on les règle dans la même passe, juste après le Top 3." Les comptes suivent la gravité RÉELLE du tableau (Critique/Haut = importants ; Moyen/Faible = légers) — dire "légers" pour du Haut/Critique est un mensonge qui coûte la confiance. Aucun important restant → formule courte "il reste {N} ajustements plus légers". Le Top 3 couvre tout → pas de ligne. Jamais de faux "c'est fini" quand la queue existe.}

## 💡 Outillage — pour aller plus loin
{JAMAIS vide. SOIT 1-2 pistes liées à l'usage observé (Q3 + mémoire) : catégorie d'outil officielle + bénéfice concret en une ligne + où l'activer + rappel données en une ligne. SOIT, si vraiment rien ne le justifie, écris : "Ton usage actuel ne justifie aucun ajout — un outil de plus serait du bruit." Choisis, écris-le.
PUIS, dans les DEUX cas, termine cette section par la question : "Veux-tu que je t'aide à trouver le meilleur outillage (skills, plugins, connecteurs) adapté à ton usage ? Je te pose 2 questions et je cherche ce qui existe vraiment."}

## 🧭 Ce que ce score ne dit pas
{limites du périmètre + honnêteté si le setup est sain mais Claude déçoit}

## 🗂️ Fichiers écartés (pas des réglages)
{chemin — raison. Vide si aucun.}

## 🧮 Détail du score
{une ligne par axe pénalisé + total. Ex : Doublons −15 (cap) · Trous −6 = −21 → 79/100}
---FIN TEMPLATE---

## Exemple rempli (fictif — calibre le format, ne le recopie pas)

# 🩺 Rapport PromptCare
**Ce que j'ai examiné :** ~/.claude/ global + projet "site-client" + historique 30 j · **Invisible d'ici :** mémoire (plan sans mémoire)
**Couverture :** 9 sources de réglages examinées (9 fichiers) · 3 écartées · 0 oublié
**Score santé : 58/100 — pollution installée : tes réglages travaillent contre toi depuis des mois.**
## 🔍 Problèmes détectés
| # | Type | Impact | Constat | Extrait |
|---|---|---|---|---|
| 1 | Contradiction | Haut | Langue contradictoire global vs projet | "Réponds en français" / "Always respond in English" |
| 2 | Obsolète | Moyen | Modèle retiré | "utilise claude-3-5-sonnet" |
| 3 | Outillage | Moyen | Skill sans trace sur la fenêtre de preuve | "pdf-export" : 0 trace sur 30 j |
## 🎯 Top 3 actions
1. Trancher la règle de langue (un seul endroit : le global)
2. Supprimer la référence au modèle retiré
3. Tester ou désinstaller "pdf-export" cette semaine
Au-delà : il reste 2 ajustements plus légers (dans le tableau ci-dessus) — on les règle dans la même passe, juste après.
## 💡 Outillage — pour aller plus loin
Tu déploies le même site client chaque semaine → un serveur MCP officiel de ton hébergeur ou de ta CI éviterait les copier-coller de logs (annuaire : marketplace officiel Claude Code). ⚠️ Un MCP accède à tes systèmes : active le minimum de permissions.
Tes rapports d'audit partent en PDF à la main → le skill de création de fichiers le fait nativement, rien à installer, demande-le simplement.
Veux-tu que je t'aide à trouver le meilleur outillage (skills, plugins, connecteurs) adapté à ton usage ? Je te pose 2 questions et je cherche ce qui existe vraiment.
## 🧭 Ce que ce score ne dit pas
La mémoire n'existe pas sur ton plan. Pour tes autres projets, relance-moi depuis le dossier parent.
## 🗂️ Fichiers écartés (pas des réglages)
README.md — doc humaine · CHANGELOG.md — historique · notes/idees.md — notes sans directives
## 🧮 Détail du score
Contradictions −15 · Doublons −10 · Obsolète −5 · Trous −6 · Bruit −4 · Outillage −2 = −42 → 58/100

## Livraison — PAR DÉFAUT, en même temps que le rapport

C'est la sortie attendue du produit, pas une option :
- **Rendu VERROUILLÉ — jamais de mise en page improvisée.** Le rapport visuel sort du gabarit `assets/rapport-template.html`, rempli par `scripts/rendu.py` (entrée = JSON, schéma documenté en tête du script ; reprends `formules` et `formule_totale` de la sortie de score.py, et les étiquettes delta dans `etiquette`/`corriges`). Couleurs, jauge de score, tableaux et l'UNIQUE animation (remplissage de la jauge, 0,9 s, désactivée à l'impression) sont figés dans le gabarit : deux rapports = même rendu.
- **Web / Desktop chat / mobile** : (1) rapport dans un ARTIFACT "🩺 Rapport PromptCare" construit à partir du HTML rendu — jamais seulement en markdown dans le fil ; (2) génère DANS LA FOULÉE le PDF depuis ce MÊME HTML (création de fichiers native — voir referentiel.md) et annonce-le ("aussi téléchargeable en PDF — dis-moi si tu le préfères en Word"). Capacité inactive → dis-le + repli : "ouvre l'artifact → Ctrl/Cmd+P → Enregistrer en PDF".
- **Claude Code** : rapport dans la conversation + crée PROMPTCARE-RAPPORT.md dans le dossier courant en l'annonçant ("supprime-le si tu n'en veux pas") ; convertisseur installé (pandoc, weasyprint, wkhtmltopdf…) → PDF depuis le HTML de rendu.py, jamais depuis le markdown brut.
- **Exécution de code indisponible** (rendu.py impossible) : reproduis le gabarit à la main dans l'artifact, avec la palette EXACTE — encre #1F2933, panneaux #F4F6F8, bordures #D9DEE4, accent #0E7C86, verdict : sains #1B7F4B · légère #B7791F · installée #C05621 · sévère #B3261E. Aucune autre couleur, aucune autre animation.
- **API** : le markdown suffit.
- La question de la section 💡 revit dans le MESSAGE DE CLÔTURE (Question 2) — ne la répète pas une 3e fois entre le rapport et la clôture.
- Le "Détail du score" du rapport recopie les formules exactes de score.py (ex. "Doublons : 2 × −5 = −10, plafonné à −15" … "100 − 39 = 61") — le lecteur doit pouvoir refaire le calcul.
