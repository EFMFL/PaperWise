"""
main.py — Point d'entrée de PaperWise.

Deux façons de lancer l'application (les deux fonctionnent) :

    streamlit run main.py      → ouvre directement l'interface web
    python3 main.py            → démarrage complet (Ollama + modèle + interface)

Dans les deux cas, Ollama est démarré automatiquement s'il ne tourne pas.
"""

import os
import runpy
import shutil
import subprocess
import sys
import time
import urllib.request

# Python où sont installées les dépendances du projet (streamlit, chromadb...)
PYTHON_PROJET = "/Library/Frameworks/Python.framework/Versions/3.12/bin/python3"
MODELE = "llama3.2:1b"
RACINE_PROJET = os.path.dirname(os.path.abspath(__file__))


def ollama_est_installe():
    return shutil.which("ollama") is not None


def ollama_tourne():
    """Vérifie si le serveur Ollama répond sur le port 11434."""
    try:
        urllib.request.urlopen("http://localhost:11434", timeout=2)
        return True
    except Exception:
        return False


def demarrer_ollama():
    print("🚀 Démarrage d'Ollama en arrière-plan...")
    with open("/tmp/ollama.log", "w") as journal:
        subprocess.Popen(
            ["ollama", "serve"],
            stdout=journal,
            stderr=journal,
            start_new_session=True,  # Ollama survit à la fermeture de ce script
        )
    # On attend qu'Ollama soit prêt (10 secondes maximum)
    for _ in range(10):
        if ollama_tourne():
            return True
        time.sleep(1)
    return False


def modele_est_telecharge():
    resultat = subprocess.run(["ollama", "list"], capture_output=True, text=True)
    return MODELE in resultat.stdout


def telecharger_modele():
    print(f"⬇️  Téléchargement du modèle {MODELE} (une seule fois)...")
    subprocess.run(["ollama", "pull", MODELE], check=True)


def preparer_ollama():
    """S'assure qu'Ollama tourne. Retourne True si tout est prêt."""
    if not ollama_est_installe():
        print("❌ Ollama n'est pas installé : https://ollama.com/download")
        return False
    if ollama_tourne():
        return True
    return demarrer_ollama()


def demarrage_complet():
    """Mode `python3 main.py` : prépare tout puis lance l'interface."""
    print("============================================")
    print("   📚 PaperWise — Démarrage")
    print("============================================")

    if not preparer_ollama():
        sys.exit(1)
    print("✅ Ollama est prêt.")

    if modele_est_telecharge():
        print(f"✅ Modèle {MODELE} déjà téléchargé.")
    else:
        telecharger_modele()

    print()
    print("🌐 Ouverture de l'interface : http://localhost:8501")
    print("   (Pour arrêter : Ctrl+C dans ce terminal)")
    print()
    subprocess.run([PYTHON_PROJET, "-m", "streamlit", "run", __file__])


def lance_par_streamlit():
    """Détecte si ce fichier a été lancé avec `streamlit run main.py`."""
    try:
        from streamlit import runtime
        return runtime.exists()
    except ImportError:
        return False


if lance_par_streamlit():
    # Mode `streamlit run main.py` : on démarre Ollama si besoin,
    # puis on affiche l'interface définie dans interface/app.py.
    preparer_ollama()
    runpy.run_path(
        os.path.join(RACINE_PROJET, "interface", "app.py"),
        run_name="__main__",
    )
elif __name__ == "__main__":
    demarrage_complet()
