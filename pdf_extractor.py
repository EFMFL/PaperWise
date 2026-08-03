"""
pdf_extractor.py
-----------------
Extrait le texte de fichiers PDF scientifiques, page par page,
en conservant les métadonnées (nom du fichier, numéro de page).
"""

import os
import fitz  # PyMuPDF
from dataclasses import dataclass
from typing import List


@dataclass
class PageDocument:
    """Représente le texte extrait d'une seule page d'un PDF."""
    source_file: str
    page_number: int
    text: str


def extract_text_from_pdf(pdf_path: str) -> List[PageDocument]:
    documents = []
    filename = os.path.basename(pdf_path)

    with fitz.open(pdf_path) as pdf:
        for page_index, page in enumerate(pdf):
            raw_text = page.get_text("text")
            cleaned_text = clean_text(raw_text)

            if cleaned_text.strip():
                documents.append(
                    PageDocument(
                        source_file=filename,
                        page_number=page_index + 1,
                        text=cleaned_text,
                    )
                )

    return documents


def clean_text(text: str) -> str:
    lines = text.split("\n")
    cleaned_lines = [line.strip() for line in lines if line.strip()]
    text = " ".join(cleaned_lines)

    while "  " in text:
        text = text.replace("  ", " ")

    return text.strip()


def extract_pdfs_from_folder(folder_path: str) -> List[PageDocument]:
    all_documents = []

    if not os.path.isdir(folder_path):
        raise FileNotFoundError(f"Dossier introuvable : {folder_path}")

    pdf_files = [f for f in os.listdir(folder_path) if f.lower().endswith(".pdf")]

    if not pdf_files:
        print(f"⚠️  Aucun fichier PDF trouvé dans {folder_path}")

    for pdf_file in pdf_files:
        pdf_path = os.path.join(folder_path, pdf_file)
        print(f"📄 Extraction de {pdf_file}...")
        documents = extract_text_from_pdf(pdf_path)
        all_documents.extend(documents)
        print(f"   → {len(documents)} pages extraites")

    return all_documents


if __name__ == "__main__":
    import sys

    folder = sys.argv[1] if len(sys.argv) > 1 else "data/pdfs"
    docs = extract_pdfs_from_folder(folder)
    print(f"\nTotal : {len(docs)} pages extraites depuis {folder}")
    if docs:
        print("\nAperçu du premier document :")
        print(f"  Fichier : {docs[0].source_file}")
        print(f"  Page : {docs[0].page_number}")
        print(f"  Texte (200 premiers caractères) : {docs[0].text[:200]}")