import os
import json
import re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOSSIER_TEXTES = os.path.join(BASE_DIR, "data", "textes_extraits")
DOSSIER_CHUNKS = os.path.join(BASE_DIR, "data", "chunks")

os.makedirs(DOSSIER_CHUNKS, exist_ok=True)

TAILLE_CHUNK = 1200
CHEVAUCHEMENT = 150


def nettoyer_texte(texte):
    texte = re.sub(r' +', ' ', texte)
    texte = re.sub(r'\n{3,}', '\n\n', texte)
    texte = re.sub(r'^\s*\d+\s*$', '', texte, flags=re.MULTILINE)
    texte = re.sub(r'\s+([,.;:!?])', r'\1', texte)
    return texte.strip()


def decouper_en_chunks(texte, taille=TAILLE_CHUNK, chevauchement=CHEVAUCHEMENT):
    if not texte:
        return []

    texte = re.sub(r'\s+', ' ', texte).strip()

    paragraphes = [p.strip() for p in re.split(r'\n{2,}|\r\n{2,}', texte) if p.strip()]
    if not paragraphes:
        paragraphes = [m.strip() for m in re.split(r'(?<=[.!?])\s+', texte) if m.strip()]

    if not paragraphes:
        return []

    chunks = []
    buffer = ""

    for paragraphe in paragraphes:
        candidat = f"{buffer} {paragraphe}".strip() if buffer else paragraphe
        if len(candidat) <= taille:
            buffer = candidat
            continue

        if buffer:
            chunks.append(buffer)
        buffer = paragraphe

    if buffer:
        chunks.append(buffer)

    chunks = [c for c in chunks if len(c.split()) >= 8 or len(c) >= 120]
    return chunks


def traiter_tous_les_textes():
    fichiers = [f for f in os.listdir(DOSSIER_TEXTES) if f.endswith(".json")]

    if not fichiers:
        print("❌ Aucun fichier JSON trouvé. Lance d'abord extraction.py !")
        return

    tous_les_chunks = []
    compteur_id = 0

    for nom_fichier in fichiers:
        chemin = os.path.join(DOSSIER_TEXTES, nom_fichier)

        with open(chemin, "r", encoding="utf-8") as f:
            data = json.load(f)

        nom_article = data["fichier"]
        print(f"✂️  Découpage de : {nom_article}")

        for page_data in data["pages"]:
            texte_propre = nettoyer_texte(page_data["texte"])
            chunks = decouper_en_chunks(texte_propre)

            for chunk in chunks:
                tous_les_chunks.append({
                    "id": f"chunk_{compteur_id}",
                    "texte": chunk,
                    "source": nom_article,
                    "page": page_data["page"]
                })
                compteur_id += 1

        print(f"   ✅ {compteur_id} chunks créés jusqu'ici")

    chemin_sortie = os.path.join(DOSSIER_CHUNKS, "tous_les_chunks.json")
    with open(chemin_sortie, "w", encoding="utf-8") as f:
        json.dump(tous_les_chunks, f, ensure_ascii=False, indent=2)

    print(f"\n🎉 {len(tous_les_chunks)} chunks sauvegardés dans {chemin_sortie}")


if __name__ == "__main__":
    traiter_tous_les_textes()
