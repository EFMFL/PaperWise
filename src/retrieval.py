import os
import chromadb
from sentence_transformers import SentenceTransformer

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOSSIER_CHROMA = os.path.join(BASE_DIR, "data", "chroma_db")
NOM_COLLECTION = "scholarag"

print("🔄 Chargement du modèle de recherche...")
modele = SentenceTransformer("all-MiniLM-L6-v2")

client = chromadb.PersistentClient(path=DOSSIER_CHROMA)
collection = client.get_or_create_collection(name=NOM_COLLECTION)
print(f"✅ Base connectée — {collection.count()} chunks disponibles\n")


def rechercher(question, nb_resultats=5, seuil_min=0.3):
    """
    Prend une question en texte et retourne les passages les plus pertinents depuis la base vectorielle.
    """
    embedding_question = modele.encode([question]).tolist()

    resultats = collection.query(
        query_embeddings=embedding_question,
        n_results=max(nb_resultats, 3),
        include=["documents", "metadatas", "distances"]
    )

    chunks_pertinents = []

    for texte, meta, distance in zip(
        resultats["documents"][0],
        resultats["metadatas"][0],
        resultats["distances"][0]
    ):
        score = round(1 - distance, 3)
        if score >= seuil_min:
            chunks_pertinents.append({
                "texte": texte,
                "source": meta.get("source", "Source inconnue"),
                "page": meta.get("page", "?"),
                "score": score
            })

    return chunks_pertinents[:nb_resultats]


def afficher_resultats(question):
    print(f"🔍 Recherche pour : '{question}'\n")
    resultats = rechercher(question)

    if not resultats:
        print("❌ Aucun passage pertinent trouvé.")
        return

    for i, r in enumerate(resultats):
        print(f"[{i+1}] Score : {r['score']} | {r['source']} — Page {r['page']}")
        print(f"     {r['texte'][:200]}...\n")


if __name__ == "__main__":
    afficher_resultats("quelles sont les méthodes utilisées dans les études ?")
