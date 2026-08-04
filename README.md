#  📚PaperWise — Chat Documentaire IA Local
PaperWise est un système RAG local permettant d’interroger des articles PDF. Il extrait, découpe et indexe les textes, puis génère des réponses ou paragraphes sourcés via un LLM local. Interface web simple, fonctionnement hors‑ligne et déploiement possible sur Raspberry Pi.


> Posez des questions à vos articles scientifiques. Obtenez des réponses sourcées, générées localement, sans internet.

![Python](https://img.shields.io/badge/Python-3.11+-blue?style=flat-square)
![Streamlit](https://img.shields.io/badge/Interface-Streamlit-red?style=flat-square)
![Ollama](https://img.shields.io/badge/LLM-Ollama%20%2F%20Mistral-green?style=flat-square)
![ChromaDB](https://img.shields.io/badge/Base%20vectorielle-ChromaDB-orange?style=flat-square)
![Licence](https://img.shields.io/badge/Licence-MIT-lightgrey?style=flat-square)

---m

## 🧠 Présentation du projet

**PaperWise** est un système RAG (Retrieval-Augmented Generation) entièrement local, conçu pour permettre à des étudiants et chercheurs d'interroger un corpus d'articles scientifiques en PDF.

Le système lit vos PDF, les découpe en passages, les indexe dans une base vectorielle, puis répond à vos questions en citant précisément les sources utilisées — le tout sans aucune connexion internet et sans envoyer vos données à un service tiers.

### Fonctionnalités principales

- 📄 **Chargement de PDF** — déposez vos articles directement dans l'interface
- 🔍 **Recherche sémantique** — retrouve les passages les plus pertinents dans votre corpus
- 🤖 **Génération locale** — utilise un LLM tournant sur votre machine (Ollama + Mistral)
- 📌 **Réponses sourcées** — chaque affirmation est accompagnée de sa référence (article, page)
- 🖥️ **Interface web** — interface simple et intuitive construite avec Streamlit
- 🍓 **Déployable sur Raspberry Pi** — fonctionne sur du matériel léger

---

## 👥 Équipe

| Membre | Rôle |
|--------|------|
| **Membre 1** | Data & Pipeline NLP (extraction PDF, embeddings, indexation Chroma) |
| **Membre 2** | IA & Génération (LLM local, prompt engineering, évaluation) |
| **Membre 3** | Interface & Déploiement (Streamlit, Raspberry Pi, documentation) |

---

## 🗂️ Structure du projet

```
PaperWise/
│
├── data/
│   ├── pdfs/               # Articles PDF scientifiques sources
│   └── chroma_db/          # Base vectorielle persistante (générée automatiquement)
│
├── src/
│   ├── extraction.py       # Extraction et nettoyage du texte des PDF (Membre 1)
│   ├── chunking.py         # Découpage en chunks et génération des embeddings (Membre 1)
│   ├── indexation.py       # Indexation dans ChromaDB (Membre 1)
│   ├── retrieval.py        # Recherche sémantique dans la base (Membre 2)
│   ├── generation.py       # Génération de réponses avec Ollama (Membre 2)
│   └── prompts.py          # Templates de prompts (Membre 2)
│
├── interface/
│   └── app.py              # Interface web Streamlit (Membre 3)
│
├── docs/
│   ├── guide_installation.md   # Guide d'installation détaillé
│   ├── guide_utilisateur.md    # Manuel d'utilisation
│   └── rapport_evaluation.md   # Rapport d'évaluation du système
│
├── tests/
│   └── questions_test.json     # Jeu de questions pour évaluer le système
│
├── requirements.txt        # Dépendances Python
├── .gitignore
└── README.md               # Ce fichier
```

---

## ⚙️ Stack technique

| Composant | Outil | Rôle |
|-----------|-------|------|
| Extraction PDF | [PyMuPDF](https://pymupdf.readthedocs.io/) | Lire et extraire le texte des PDF |
| Découpage | LangChain `RecursiveCharacterTextSplitter` | Créer des chunks de 400 mots avec chevauchement |
| Embeddings | `sentence-transformers` (`all-MiniLM-L6-v2`) | Transformer le texte en vecteurs numériques |
| Base vectorielle | [ChromaDB](https://www.trychroma.com/) | Stocker et interroger les embeddings |
| LLM local | [Ollama](https://ollama.com/) + Mistral 7B | Générer les réponses |
| Interface | [Streamlit](https://streamlit.io/) | Interface web locale |
| Déploiement | Raspberry Pi 4 (4 Go RAM) | Hébergement local sans serveur externe |

---

## 🚀 Installation

### Prérequis

- Python 3.11 ou supérieur
- [Ollama](https://ollama.com/) installé sur votre machine
- Git

### Étape 1 — Cloner le dépôt

```bash
git clone https://github.com/votre-organisation/scholaRAG.git
cd PaperWise
```

### Étape 2 — Créer un environnement virtuel (recommandé)

```bash
python -m venv venv

# Sur Windows :
venv\Scripts\activate

# Sur Mac/Linux :
source venv/bin/activate
```

### Étape 3 — Installer les dépendances Python

```bash
pip install -r requirements.txt
```

### Étape 4 — Télécharger le modèle de langage

```bash
# Modèle recommandé (PC avec 8 Go RAM minimum) :
ollama pull mistral

# Modèle léger (Raspberry Pi ou PC limité) :
ollama pull tinyllama
```

### Étape 5 — Lancer Ollama en arrière-plan

```bash
ollama serve
```

> Laissez ce terminal ouvert. Ollama doit tourner pour que le système fonctionne.

### Étape 6 — Lancer l'interface

```bash
streamlit run interface/app.py
```

L'interface s'ouvre automatiquement dans votre navigateur à l'adresse : **http://localhost:8501**

---

## 📖 Utilisation

### 1. Déposer vos articles PDF

Dans l'interface Streamlit, cliquez sur **"Dépose tes articles PDF ici"** et sélectionnez un ou plusieurs fichiers PDF. Le système extrait et indexe automatiquement leur contenu.

> ⚠️ Cette étape peut prendre quelques minutes selon le nombre d'articles. Elle n'est nécessaire qu'une seule fois — la base est sauvegardée sur le disque.

### 2. Poser une question

Tapez votre question dans la zone de chat et appuyez sur **Entrée** ou cliquez sur **Envoyer**.

Exemple de questions :
- *"Quels sont les effets de la température sur la biodiversité marine ?"*
- *"Quelles méthodes d'apprentissage automatique sont utilisées pour la détection d'anomalies ?"*
- *"Résume les conclusions principales de l'article sur le changement climatique."*

### 3. Lire la réponse et les sources

La réponse générée apparaît dans le chat, accompagnée des **sources utilisées** : nom de l'article, numéro de page, et extrait du passage.

---

## 🍓 Déploiement sur Raspberry Pi

### Matériel requis

- Raspberry Pi 4 avec **4 Go de RAM minimum**
- Carte microSD 32 Go (classe 10 recommandée)
- Accès au réseau local (Wi-Fi ou Ethernet)

### Instructions

```bash
# 1. Cloner le projet sur le Pi
git clone https://github.com/votre-organisation/PaperWise.git
cd PaperWise

# 2. Installer les dépendances
pip install -r requirements.txt

# 3. Installer Ollama pour ARM
curl -fsSL https://ollama.com/install.sh | sh

# 4. Télécharger un modèle léger
ollama pull tinyllama

# 5. Lancer l'interface accessible sur le réseau local
streamlit run interface/app.py --server.address 0.0.0.0 --server.port 8501
```

L'interface est alors accessible depuis n'importe quel appareil sur le même réseau Wi-Fi à l'adresse **http://[IP-du-Pi]:8501**.

> Pour trouver l'adresse IP du Pi : tapez `hostname -I` dans son terminal.

---

## 📊 Évaluation

Le système a été évalué sur un jeu de 20 questions issues du corpus d'articles, selon les critères suivants :

| Critère | Description |
|---------|-------------|
| **Fidélité** | La réponse est-elle fondée sur les documents (pas d'invention) ? |
| **Pertinence du retrieval** | Les bons passages ont-ils été retrouvés ? |
| **Qualité de génération** | La réponse est-elle claire, cohérente et bien rédigée ? |
| **Précision des citations** | Les sources citées sont-elles correctes ? |

Les résultats détaillés sont disponibles dans [`docs/rapport_evaluation.md`](docs/rapport_evaluation.md).

---

## 📁 Dépendances (`requirements.txt`)

```
pymupdf>=1.23.0
sentence-transformers>=2.7.0
chromadb>=0.5.0
langchain>=0.2.0
langchain-community>=0.2.0
ollama>=0.2.0
streamlit>=1.35.0
ragas>=0.1.0
```

Générez ce fichier automatiquement après installation avec :

```bash
pip freeze > requirements.txt
```

---

## 🤝 Contribuer au projet

### Workflow Git recommandé

```bash
# 1. Toujours partir d'une branche à jour
git checkout main
git pull origin main

# 2. Créer une branche pour votre fonctionnalité
git checkout -b feature/nom-de-la-fonctionnalite

# 3. Faire vos modifications, puis committer
git add .
git commit -m "feat: description courte de ce que tu as fait"

# 4. Pousser et créer une Pull Request sur GitHub
git push origin feature/nom-de-la-fonctionnalite
```

### Convention de nommage des commits

| Préfixe | Usage |
|---------|-------|
| `feat:` | Nouvelle fonctionnalité |
| `fix:` | Correction de bug |
| `docs:` | Modification de la documentation |
| `test:` | Ajout ou modification de tests |
| `refactor:` | Amélioration du code sans changer le comportement |

### Branches principales

- `main` — version stable, toujours fonctionnelle
- `dev` — branche d'intégration, pour tester avant de merger dans main
- `feature/xxx` — branches de fonctionnalités individuelles

---

## ❓ Problèmes fréquents

**Ollama ne répond pas**
```bash
# Vérifiez qu'Ollama tourne bien :
ollama list
# Si rien ne s'affiche, relancez : ollama serve
```

**Le PDF ne s'indexe pas**
> Vérifiez que le PDF n'est pas un scan (image). PyMuPDF ne peut pas lire le texte dans une image. Utilisez un PDF avec du texte sélectionnable.

**L'interface est lente sur Raspberry Pi**
> Utilisez le modèle `tinyllama` à la place de `mistral`. Vous pouvez aussi héberger Ollama sur un PC plus puissant et y connecter le Pi via le réseau.

**Erreur `ModuleNotFoundError`**
```bash
# Vérifiez que votre environnement virtuel est bien activé :
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows

# Puis réinstallez les dépendances :
pip install -r requirements.txt
```

---

## 📄 Licence

Ce projet est distribué sous licence **MIT**. Vous êtes libres de l'utiliser, le modifier et le partager, à condition de citer les auteurs originaux.

---

## 🙏 Remerciements

- [Mohamed AAZI](https://github.com/) — pour la définition du sujet et l'encadrement du projet
- [Ollama](https://ollama.com/) — pour avoir rendu les LLM locaux accessibles à tous
- [ChromaDB](https://www.trychroma.com/) — base vectorielle open-source légère et efficace
- [Streamlit](https://streamlit.io/) — pour la simplicité de création d'interfaces web en Python

---

*Projet réalisé dans le cadre d'un programme de formation en Data & IA — 2025/2026*
