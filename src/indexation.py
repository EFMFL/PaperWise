import json
import os

try:
    import chromadb
except ImportError:
    chromadb = None

try:
    from sentence_transformers import SentenceTransformer
except ImportError:
    SentenceTransformer = None

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FICHIER_CHUNKS = os.path.join(BASE_DIR, "data", "chunks", "tous_les_chunks.json")
DOSSIER_CHROMA = os.path.join(BASE_DIR, "data", "chroma_db")

modele = None
collection = None


def _initialiser_client_et_modele():
    global modele, collection

    if modele is None:
        if SentenceTransformer is None:
            raise ImportError("sentence-transformers n'est pas installé")
        print("🔄 Chargement du modèle d'embeddings...")
        modele = SentenceTransformer("all-MiniLM-L6-v2")
        print("✅ Modèle chargé !\n")

    if collection is None:
        if chromadb is None:
            raise ImportError("chromadb n'est pas installé")
        client = chromadb.PersistentClient(path=DOSSIER_CHROMA)
        collection = client.get_or_create_collection(
            name="scholarag",
            metadata={"hnsw:space": "cosine"}
        )


def indexer_chunks():
    _initialiser_client_et_modele()

    with open(FICHIER_CHUNKS, "r", encoding="utf-8") as f:
        chunks = json.load(f)

    print(f"📦 {len(chunks)} chunks à indexer...\n")
    taille_lot = 20

    for i in range(0, len(chunks), taille_lot):
        lot = chunks[i:i + taille_lot]

        ids = [c["id"] for c in lot]
        textes = [c["texte"] for c in lot]
        metadonnees = [{"source": c["source"], "page": c["page"]} for c in lot]

        embeddings_brut = modele.encode(textes, show_progress_bar=False)
        if hasattr(embeddings_brut, "tolist"):
            embeddings = embeddings_brut.tolist()
        else:
            embeddings = embeddings_brut

        collection.upsert(
            ids=ids,
            documents=textes,
            embeddings=embeddings,
            metadatas=metadonnees
        )

        print(f"  ✅ Lot {i // taille_lot + 1} indexé ({min(i + taille_lot, len(chunks))}/{len(chunks)} chunks)")

    print(f"\n🎉 Indexation terminée ! Base sauvegardée dans : {DOSSIER_CHROMA}")
    print(f"📊 Total dans la base : {collection.count()} chunks")


def tester_recherche():
    _initialiser_client_et_modele()

    print("\n🔍 Test de recherche...")
    question_test = "méthodes d'apprentissage automatique"

    embedding_question = modele.encode([question_test]).tolist()

    resultats = collection.query(
        query_embeddings=embedding_question,
        n_results=3
    )

    print(f"Question test : '{question_test}'")
    print("\nTop 3 passages trouvés :\n")

    for j, (doc, meta) in enumerate(zip(resultats["documents"][0], resultats["metadatas"][0])):
        print(f"  [{j+1}] Source : {meta['source']} — Page {meta['page']}")
        print(f"       Extrait : {doc[:150]}...\n")


if __name__ == "__main__":
    indexer_chunks()
    tester_recherche()
