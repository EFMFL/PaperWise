"""
app.py — Interface web Streamlit de PaperWise (Membre 3)
---------------------------------------------------------
Interface de chat qui permet de :
1. Déposer des articles PDF
2. Les indexer dans la base vectorielle (pipeline du Membre 1)
3. Poser des questions et obtenir des réponses sourcées (pipeline du Membre 2)

Lancement (depuis la racine du projet) :
    streamlit run interface/app.py
"""

import os
import sys

import streamlit as st

# Le projet utilise des chemins relatifs à la racine (ex: "data/pdfs").
# On se place donc à la racine du projet, peu importe d'où l'app est lancée.
RACINE_PROJET = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(RACINE_PROJET)
if RACINE_PROJET not in sys.path:
    sys.path.insert(0, RACINE_PROJET)

DOSSIER_PDFS = os.path.join(RACINE_PROJET, "data", "pdfs")
os.makedirs(DOSSIER_PDFS, exist_ok=True)


# ---------------------------------------------------------------------------
# Configuration de la page
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="PaperWise — Chat documentaire",
    page_icon="📚",
    layout="wide",
)


# ---------------------------------------------------------------------------
# Fonctions utilitaires
# ---------------------------------------------------------------------------
@st.cache_resource(show_spinner=False)
def charger_moteur_recherche():
    """Charge le module de recherche une seule fois (le modèle d'embeddings
    met quelques secondes à se charger)."""
    from src import retrieval
    return retrieval


def indexer_les_documents():
    """Lance le pipeline complet : extraction -> chunking -> indexation."""
    from src.extraction import traiter_tous_les_pdfs
    from src.chunking import traiter_tous_les_textes

    with st.status("Indexation en cours...", expanded=True) as statut:
        st.write("1/3 — Extraction du texte des PDF...")
        traiter_tous_les_pdfs()

        st.write("2/3 — Découpage du texte en chunks...")
        traiter_tous_les_textes()

        st.write("3/3 — Indexation dans la base vectorielle...")
        from src.indexation import indexer_chunks
        indexer_chunks()

        statut.update(label="Indexation terminée !", state="complete", expanded=False)


def nombre_de_chunks_indexes():
    """Retourne le nombre de passages actuellement indexés dans ChromaDB."""
    try:
        retrieval = charger_moteur_recherche()
        return retrieval.collection.count()
    except Exception:
        return 0


# ---------------------------------------------------------------------------
# Barre latérale : gestion des documents
# ---------------------------------------------------------------------------
with st.sidebar:
    st.title("📚 PaperWise")
    st.caption("Chat documentaire 100 % local — vos données ne quittent pas votre machine.")

    st.header("1. Déposer vos PDF")
    fichiers = st.file_uploader(
        "Dépose tes articles PDF ici",
        type="pdf",
        accept_multiple_files=True,
    )

    if fichiers:
        for fichier in fichiers:
            chemin = os.path.join(DOSSIER_PDFS, fichier.name)
            with open(chemin, "wb") as f:
                f.write(fichier.getbuffer())
        st.success(f"{len(fichiers)} fichier(s) enregistré(s) dans data/pdfs/")

    st.header("2. Indexer les documents")
    if st.button("🔄 Lancer l'indexation", use_container_width=True):
        indexer_les_documents()

    nb_chunks = nombre_de_chunks_indexes()
    if nb_chunks > 0:
        st.info(f"Base vectorielle : **{nb_chunks} passages** indexés.")
    else:
        st.warning("Base vectorielle vide. Dépose des PDF puis lance l'indexation.")

    st.divider()
    st.caption(
        "⚠️ Ollama doit tourner en arrière-plan (`ollama serve`) "
        "pour que la génération fonctionne."
    )


# ---------------------------------------------------------------------------
# Zone principale : le chat
# ---------------------------------------------------------------------------
st.title("💬 Posez vos questions à vos documents")

# L'historique de la conversation est conservé dans la session Streamlit
if "messages" not in st.session_state:
    st.session_state.messages = []

# On réaffiche tout l'historique à chaque rechargement de la page
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message.get("sources"):
            with st.expander(f"📌 Sources utilisées ({len(message['sources'])})"):
                for i, source in enumerate(message["sources"], start=1):
                    st.markdown(
                        f"**[Source {i}]** `{source['source']}` — "
                        f"page {source['page']} (score : {source['score']})"
                    )
                    st.caption(source["texte"][:300] + "...")

# Zone de saisie de la question
question = st.chat_input("Exemple : Quelles sont les conclusions principales de l'article ?")

if question:
    # 1. On affiche la question de l'utilisateur
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    # 2. On génère la réponse avec le module du Membre 2
    with st.chat_message("assistant"):
        with st.spinner("Recherche dans les documents et génération de la réponse..."):
            try:
                from src.generation import generer_reponse
                resultat = generer_reponse(question)
                reponse = resultat["reponse"]
                sources = resultat["sources"]
            except Exception as erreur:
                reponse = (
                    "❌ Une erreur est survenue pendant la génération. "
                    "Vérifie qu'Ollama est bien lancé (`ollama serve`) et que "
                    f"des documents sont indexés.\n\nDétail : `{erreur}`"
                )
                sources = []

        st.markdown(reponse)

        if sources:
            with st.expander(f"📌 Sources utilisées ({len(sources)})"):
                for i, source in enumerate(sources, start=1):
                    st.markdown(
                        f"**[Source {i}]** `{source['source']}` — "
                        f"page {source['page']} (score : {source['score']})"
                    )
                    st.caption(source["texte"][:300] + "...")

    # 3. On sauvegarde la réponse dans l'historique
    st.session_state.messages.append(
        {"role": "assistant", "content": reponse, "sources": sources}
    )
