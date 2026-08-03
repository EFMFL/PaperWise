"""
vector_store.py
-----------------
Gère l'indexation et la recherche sémantique via ChromaDB.
"""

import chromadb
from chromadb.utils import embedding_functions
from typing import List
from chunking import Chunk


class VectorStore:
    def __init__(
        self,
        persist_directory: str = "data/chroma_db",
        collection_name: str = "articles_scientifiques",
        embedding_model: str = "all-MiniLM-L6-v2",
    ):
        self.client = chromadb.PersistentClient(path=persist_directory)

        self.embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name=embedding_model
        )

        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            embedding_function=self.embedding_function,
        )

    def index_chunks(self, chunks: List[Chunk]) -> None:
        if not chunks:
            print("⚠️  Aucun chunk à indexer.")
            return

        self.collection.add(
            ids=[c.chunk_id for c in chunks],
            documents=[c.text for c in chunks],
            metadatas=[
                {"source_file": c.source_file, "page_number": c.page_number}
                for c in chunks
            ],
        )
        print(f"✅ {len(chunks)} chunks indexés dans la base vectorielle.")

    def search(self, query: str, top_k: int = 5) -> List[dict]:
        results = self.collection.query(
            query_texts=[query],
            n_results=top_k,
        )

        formatted_results = []
        documents = results["documents"][0]
        metadatas = results["metadatas"][0]
        distances = results["distances"][0]

        for text, meta, distance in zip(documents, metadatas, distances):
            formatted_results.append(
                {
                    "text": text,
                    "source_file": meta["source_file"],
                    "page_number": meta["page_number"],
                    "distance": distance,
                }
            )

        return formatted_results

    def count(self) -> int:
        return self.collection.count()


if __name__ == "__main__":
    from pdf_extractor import extract_pdfs_from_folder
    from chunking import chunk_documents

    docs = extract_pdfs_from_folder("data/pdfs")
    chunks = chunk_documents(docs)

    store = VectorStore()
    store.index_chunks(chunks)
    print("Nombre total de chunks dans la base :", store.count())
    query = "What happens to the lake elevation by 2050?"
    results = store.search(query, top_k=3)
    print("Résultats pour :", query)
    for r in results:
        print("-", r["source_file"], "page", r["page_number"], ":", r["text"][:100])
    