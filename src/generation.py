import os
import sys
import ollama

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from src.prompts import construire_prompt, construire_prompt_resume

MODELES_CANDIDATS = [
    os.getenv("OLLAMA_MODEL", "").strip() or "llama3.2:1b",
    "mistral",
    "llama3.2",
    "phi3",
]


def _extraire_noms_modeles(reponse):
    if not isinstance(reponse, dict):
        return []

    models = reponse.get("models") or []
    noms = []
    for item in models:
        if isinstance(item, str):
            noms.append(item)
        elif isinstance(item, dict):
            for key in ("name", "model"):
                valeur = item.get(key)
                if isinstance(valeur, str) and valeur:
                    noms.append(valeur)
    return noms


def _obtenir_modele():
    priorites = []
    for modele in MODELES_CANDIDATS:
        if modele and modele not in priorites:
            priorites.append(modele)

    try:
        noms_installes = _extraire_noms_modeles(ollama.list())
    except Exception as exc:
        noms_installes = []
        print(f"⚠️ Impossible de lister les modèles Ollama : {exc}")

    for modele in priorites:
        if modele in noms_installes:
            return modele

    for modele in priorites:
        try:
            print(f"📥 Téléchargement du modèle {modele}...")
            ollama.pull(modele)
            return modele
        except Exception as exc:
            print(f"⚠️ Impossible de télécharger {modele} : {exc}")

    return priorites[0]


def _generer_avec_modele(prompt, modele):
    try:
        reponse_modele = ollama.chat(
            model=modele,
            messages=[{"role": "user", "content": prompt}]
        )
        return reponse_modele["message"]["content"]
    except Exception as exc:
        print(f"⚠️ Génération Ollama impossible : {exc}")

        if "404" in str(exc):
            print(f"⚠️ Le modèle {modele} n'est pas disponible, tentative avec un autre modèle...")
            for candidat in MODELES_CANDIDATS:
                if candidat == modele:
                    continue
                try:
                    reponse_modele = ollama.chat(
                        model=candidat,
                        messages=[{"role": "user", "content": prompt}]
                    )
                    return reponse_modele["message"]["content"]
                except Exception:
                    continue

        contextes = []
        for ligne in prompt.splitlines():
            if ligne.startswith("[Source"):
                contextes.append(ligne)
        if contextes:
            return (
                "Réponse générée localement à partir des passages récupérés. "
                "Le moteur Ollama n'a pas pu produire une réponse complète, mais les informations suivantes sont extraites du document indexé."
            )

        return "Le moteur local de génération n'est pas disponible actuellement."


def generer_reponse(question, nb_chunks=5):
    """
    Fonction principale : prend une question et retourne
    une réponse complète avec les sources utilisées.
    """
    from src.retrieval import rechercher

    print(f"\n📨 Question reçue : {question}")

    print("🔍 Recherche des passages pertinents...")
    chunks = rechercher(question, nb_resultats=nb_chunks)

    if not chunks:
        return {
            "reponse": "Je ne trouve pas d'informations dans les documents indexés. "
                       "Vérifie qu'au moins un PDF a été indexé.",
            "sources": [],
            "question": question
        }

    print(f"✅ {len(chunks)} passages trouvés")

    prompt = construire_prompt(question, chunks)
    modele = _obtenir_modele()

    print(f"🤖 Génération de la réponse avec {modele}...")
    texte_reponse = _generer_avec_modele(prompt, modele)

    if not texte_reponse.strip():
        texte_reponse = (
            "Aucune réponse n'a pu être générée automatiquement. "
            "Le document contient cependant des passages pertinents qui ont été récupérés."
        )

    print("✅ Réponse générée !\n")

    return {
        "reponse": texte_reponse,
        "sources": chunks,
        "question": question
    }


def generer_resume(nom_article):
    """
    Génère un résumé structuré d'un article spécifique.
    """
    from src.retrieval import rechercher

    chunks = rechercher(nom_article, nb_resultats=10)
    chunks_article = [c for c in chunks if nom_article.lower() in c["source"].lower()]

    if not chunks_article:
        return f"Article '{nom_article}' non trouvé dans la base."

    prompt = construire_prompt_resume(chunks_article, nom_article)
    modele = _obtenir_modele()
    reponse = ollama.chat(model=modele, messages=[{"role": "user", "content": prompt}])

    return reponse["message"]["content"]


def afficher_reponse_complete(question):
    resultat = generer_reponse(question)

    print("=" * 60)
    print(f"QUESTION : {resultat['question']}")
    print("=" * 60)
    print(f"\nRÉPONSE :\n{resultat['reponse']}")
    print("\n" + "-" * 60)
    print("SOURCES UTILISÉES :")
    for i, source in enumerate(resultat["sources"]):
        print(f"  [{i+1}] {source['source']} — Page {source['page']} (score: {source['score']})")
    print("=" * 60)


if __name__ == "__main__":
    afficher_reponse_complete("Quelles sont les principales méthodes utilisées dans les études ?")
