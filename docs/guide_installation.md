# Guide d'installation — PaperWise

Ce guide explique comment installer PaperWise sur votre machine, étape par étape.

## Prérequis

- **Python 3.11 ou supérieur** — vérifiez avec `python3 --version`
- **Git** — vérifiez avec `git --version`
- **[Ollama](https://ollama.com/download)** — le moteur qui fait tourner le modèle de langage en local

## Étape 1 — Cloner le dépôt

```bash
git clone https://github.com/EFMFL/PaperWise.git
cd PaperWise
```

## Étape 2 — Créer un environnement virtuel

Un environnement virtuel isole les dépendances du projet du reste de votre machine.

```bash
python3 -m venv venv

# Sur Mac/Linux :
source venv/bin/activate

# Sur Windows :
venv\Scripts\activate
```

> Votre invite de commande doit maintenant afficher `(venv)` au début de la ligne.

## Étape 3 — Installer les dépendances Python

```bash
pip install -r requirements.txt
```

> ⏳ Cette étape peut prendre plusieurs minutes : `sentence-transformers` télécharge
> des bibliothèques volumineuses (PyTorch notamment).

## Étape 4 — Installer et lancer Ollama

1. Téléchargez Ollama depuis [ollama.com/download](https://ollama.com/download) et installez-le.
2. Téléchargez un modèle de langage :

```bash
# Modèle recommandé (PC avec 8 Go de RAM minimum) :
ollama pull mistral

# Modèle léger (machine limitée ou Raspberry Pi) :
ollama pull llama3.2:1b
```

3. Lancez le serveur Ollama et **laissez ce terminal ouvert** :

```bash
ollama serve
```

> Si vous obtenez une erreur « address already in use », c'est qu'Ollama tourne
> déjà en arrière-plan : tout va bien, passez à la suite.

## Étape 5 — Lancer l'interface web

Dans un **nouveau terminal**, à la racine du projet (avec le venv activé) :

```bash
streamlit run interface/app.py
```

L'interface s'ouvre automatiquement dans votre navigateur à l'adresse
**http://localhost:8501**.

## Vérification rapide

1. Dans la barre latérale, déposez un PDF (avec du texte sélectionnable, pas un scan).
2. Cliquez sur **« Lancer l'indexation »** et attendez la fin des 3 étapes.
3. Posez une question dans la zone de chat : la réponse doit citer ses sources.

## Problèmes fréquents

| Problème | Solution |
| --- | --- |
| `ModuleNotFoundError` | Vérifiez que le venv est activé (`source venv/bin/activate`), puis relancez `pip install -r requirements.txt`. |
| Ollama ne répond pas | Vérifiez avec `ollama list` que le serveur tourne. Sinon, relancez `ollama serve`. |
| Le PDF ne s'indexe pas | Le PDF est peut-être un scan (image). Utilisez un PDF avec du texte sélectionnable. |
| Réponse très lente | Utilisez un modèle plus léger : `ollama pull llama3.2:1b`. |
