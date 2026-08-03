"""
chunking.py
------------
Découpe les documents (pages de PDF) en morceaux de texte (chunks)
adaptés à l'indexation vectorielle.
"""

from dataclasses import dataclass
from typing import List
from pdf_extractor import PageDocument


@dataclass
class Chunk:
    """Un morceau de texte prêt à être indexé, avec ses métadonnées de source."""
    chunk_id: str
    text: str
    source_file: str
    page_number: int


def split_text_into_words(text: str) -> List[str]:
    return text.split(" ")


def chunk_documents(
    documents: List[PageDocument],
    chunk_size: int = 500,
    overlap: int = 50,
) -> List[Chunk]:
    all_chunks = []
    chunk_counter = 0

    for doc in documents:
        words = split_text_into_words(doc.text)

        if len(words) <= chunk_size:
            chunk_counter += 1
            all_chunks.append(
                Chunk(
                    chunk_id=f"chunk_{chunk_counter}",
                    text=doc.text,
                    source_file=doc.source_file,
                    page_number=doc.page_number,
                )
            )
            continue

        start = 0
        step = chunk_size - overlap

        while start < len(words):
            end = start + chunk_size
            chunk_words = words[start:end]
            chunk_text = " ".join(chunk_words)

            chunk_counter += 1
            all_chunks.append(
                Chunk(
                    chunk_id=f"chunk_{chunk_counter}",
                    text=chunk_text,
                    source_file=doc.source_file,
                    page_number=doc.page_number,
                )
            )

            start += step

    return all_chunks


if __name__ == "__main__":
    from pdf_extractor import extract_pdfs_from_folder

    docs = extract_pdfs_from_folder("data/pdfs")
    chunks = chunk_documents(docs)
    print(f"{len(docs)} pages → {len(chunks)} chunks")
    if chunks:
        print(f"\nExemple de chunk :\n{chunks[0]}")