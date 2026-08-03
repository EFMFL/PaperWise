import json
import os
import chromadb
from sentence_transformers import SentenceTransformer

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FICHIER_CHUNKS = os.path.join(BASE_DIR, "data", "chunks", "tous_les_chunks.json")
DOSSIER_CHROMA = os.path.join(BASE_DIR, "data", "chroma_db")

print("🔄 Chargement du modèle d'embeddings...")
modele = SentenceTransformer("all-MiniLM-L6-v2")
print("✅ Modèle chargé !\n")

client = chromadb.PersistentClient(path=DOSSIER_CHROMA)
collection = client.get_or_create_collection(
    name="scholarag",
    metadata={"hnsw:space": "cosine"}
)


def indexer_chunks():
    with open(FICHIER_CHUNKS, "r", encoding="utf-8") as f:
        chunks = json.load(f)

    # Nettoyage : on retire de la base les chunks qui n'existent plus
    # (sinon les documents supprimés continueraient d'apparaître dans les réponses)
    ids_actuels = {c["id"] for c in chunks}
    ids_en_base = collection.get(include=[])["ids"]
    ids_obsoletes = [i for i in ids_en_base if i not in ids_actuels]
    if ids_obsoletes:
        collection.delete(ids=ids_obsoletes)
        print(f"🧹 {len(ids_obsoletes)} anciens chunks supprimés de la base")

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
