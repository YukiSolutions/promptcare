# 🩺 PromptCare : le check-up de ta configuration Claude

**Un plugin gratuit de [Yuki Solutions](https://www.yukisolutions.fr).** En français, pensé pour ton Claude de tous les jours, pas pour les développeurs.

Tu utilises Claude depuis des mois ? Sans t'en rendre compte, tu as accumulé des réglages : instructions, mémoire, projets, fichiers CLAUDE.md, skills, connecteurs. Ça grossit, ça finit par se contredire, vieillir, se répéter. Et Claude répond à côté sans que tu saches pourquoi.

PromptCare examine tout ça et te rend :
- un **score de santé sur 100**, calculé selon un barème écrit, avec les formules affichées,
- la **liste de ce qui cloche**, du plus grave au plus léger, avec citations,
- le **top 3 des corrections** à faire en priorité,
- un **rapport téléchargeable** (PDF/Markdown).

Il ne modifie, ne crée et ne supprime **jamais rien sans ton accord explicite**.

## Installation

Deux chemins selon la façon dont tu utilises Claude.

### Claude Desktop / Web (plans payants) — sans ligne de commande, en 2 minutes

1. Ouvre les **Paramètres** → **Plugins** (tout en bas de la barre de gauche, section « Personnaliser ») → clique **Ajouter**, en haut à droite.
2. Choisis **Ajouter une marketplace**, puis **Ajouter depuis un dépôt**.
3. Colle cette adresse dans le champ URL, puis clique **Synchro** :
   `https://github.com/YukiSolutions/promptcare.git`
   (L'avertissement rouge est normal : Anthropic l'affiche pour tout plugin qui ne vient pas de ses propres sources. Tu installes ici le dépôt officiel de Yuki Solutions.)
4. **PromptCare by Yuki Solutions** apparaît dans ta liste : la marketplace est synchronisée, mais le plugin n'est pas encore installé. Sur sa carte, clique le **« + »** en haut à droite. Il se transforme en roue crantée : installé et actif.

### Claude Code

```
/plugin marketplace add YukiSolutions/promptcare
/plugin install promptcare@yuki
```

Le guide illustré pas à pas, captures d'écran à l'appui : **[yukisolutions.fr](https://www.yukisolutions.fr)**.

## Utilisation

Tape `/promptcare`, ou demande simplement « fais le check-up de mes réglages Claude ».

3 questions rapides, puis l'audit se déroule tout seul. Compte 2 à 10 minutes selon la taille de ta configuration.

Conseils : lance chaque audit dans une **conversation neuve**, quand ton **quota d'usage est encore plein**. L'audit fonctionne très bien avec tes réglages habituels : inutile de changer de modèle ou de pousser des curseurs pour lui.

## D'un audit à l'autre : pourquoi les résultats peuvent varier

Deux audits sur les mêmes réglages peuvent différer légèrement. C'est normal, et voici pourquoi : le score suit toujours le même barème, mais la **lecture de tes réglages reste un exercice de jugement** mené par une IA. Comme deux relecteurs humains, deux passages peuvent classer un cas limite un peu différemment, en particulier si le **modèle** ou l'**effort de réflexion** (le réglage Faible / Moyen / Élevé / Extra / Max, quand il existe chez toi) n'est pas le même.

Ce qui ne bouge pas : les problèmes importants ressortent à chaque passage, avec leurs citations exactes pour que tu vérifies toi-même. L'écart normal se compte en quelques points, jamais en changement de diagnostic.

Deux repères simples :
- **Pour suivre tes progrès dans le temps** : garde les mêmes conditions d'un audit à l'autre (même modèle, même effort, conversation neuve). C'est l'évolution qui compte, pas le chiffre absolu.
- **Pas besoin de forcer** : un modèle plus puissant ou un effort plus élevé rend l'analyse un peu plus stable, mais consomme ton quota plus vite. Sur un plan à 20 €, reste sur tes réglages par défaut : l'audit y est déjà fiable.

## Ce que contient le plugin

| Composant | Rôle |
|---|---|
| `/promptcare` (compétence) | Lance le check-up avec la méthode complète : s'adapte à chaque endroit d'où tu utilises Claude, barème verrouillé |
| 2 assistants internes | Examen des gros volumes de fichiers · vérification en ligne des outils avant toute recommandation |
| `score.py` + `rendu.py` | Score calculé par du code (formules affichées, refaisables à la main) et rapport rendu depuis un gabarit figé : le même barème et le même rendu à chaque audit |
| Rappel automatique (Cowork/Code) | Te suggère un nouveau check-up si le précédent date de plus de 30 jours |

## Ce que PromptCare peut et ne peut pas faire

**Il peut :**
- lire tes réglages Claude (instructions, mémoire, projets, fichiers) pour les examiner avec toi ;
- calculer le score avec un script embarqué : formules affichées, refaisables à la main ;
- vérifier en ligne qu'un outil qu'il te recommande existe toujours (recherche publique classique, sans rien y joindre de tes données) ;
- te proposer des corrections, que tu acceptes ou refuses une par une.

**Il ne peut pas :**
- envoyer tes données à l'extérieur : pas de télémétrie, pas de compte, pas de serveur chez Yuki Solutions, tout se passe dans ta conversation ;
- modifier, créer ou supprimer quoi que ce soit sans ton accord explicite, correction par correction ;
- lancer un audit sans toi : même le rappel des 30 jours ne fait que te le proposer.

Les seules écritures (note de suivi d'audit, rapport) se font chez toi, avec ton accord, et tu peux les supprimer à tout moment. Le code est public, sous licence MIT : tout ceci se vérifie sur le dépôt.

**Développeur avec Claude Code ?** La commande native `/doctor` y vérifie déjà l'installation technique (version, mises à jour, fichiers trop lourds) : garde-la pour ça. PromptCare audite autre chose : le contenu de tes réglages, ce qui se contredit, se répète ou a vieilli. Là où aucun outil natif ne va. Les deux se complètent.

## Guide complet & mises à jour

Le guide « où lancer PromptCare selon ton cas » et les mises à jour du référentiel :
**[yukisolutions.fr](https://www.yukisolutions.fr)**

---
© Yuki Solutions · Licence MIT
