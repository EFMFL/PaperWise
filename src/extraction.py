import fitz
import os
import json

DOSSIER_PDFS = "data/pdfs"
DOSSIER_SORTIE = "data/textes_extraits"

os.makedirs(DOSSIER_SORTIE, exist_ok=True)


def extraire_texte_pdf(chemin_pdf):
    document = fitz.open(chemin_pdf)
    pages = []

    for numero_page in range(len(document)):
        page = document[numero_page]
        texte = page.get_text()
        if texte.strip():
            pages.append({"page": numero_page + 1, "texte": texte})

    document.close()
    return pages


def supprimer_textes_orphelins(fichiers_pdf):
    """Supprime les JSON dont le PDF d'origine n'existe plus dans data/pdfs.

    Sans ce nettoyage, un PDF supprimé continuerait d'être réindexé
    à chaque indexation (son texte extrait resterait sur le disque).
    """
    pdfs_presents = set(fichiers_pdf)
    for nom_json in os.listdir(DOSSIER_SORTIE):
        if not nom_json.endswith(".json"):
            continue
        pdf_correspondant = nom_json[:-len(".json")] + ".pdf"
        if pdf_correspondant not in pdfs_presents:
            os.remove(os.path.join(DOSSIER_SORTIE, nom_json))
            print(f"  🧹 Ancien texte supprimé (PDF disparu) : {nom_json}")


def traiter_tous_les_pdfs():
    fichiers_pdf = [f for f in os.listdir(DOSSIER_PDFS) if f.endswith(".pdf")]

    supprimer_textes_orphelins(fichiers_pdf)

    if not fichiers_pdf:
        print("❌ Aucun PDF trouvé dans data/pdfs/ !")
        return

    print(f"📄 {len(fichiers_pdf)} PDF trouvé(s). Début de l'extraction...\n")

    for nom_fichier in fichiers_pdf:
        chemin = os.path.join(DOSSIER_PDFS, nom_fichier)
        print(f"  → Traitement de : {nom_fichier}")

        pages = extraire_texte_pdf(chemin)
        nom_sortie = nom_fichier.replace(".pdf", ".json")
        chemin_sortie = os.path.join(DOSSIER_SORTIE, nom_sortie)

        resultat = {
            "fichier": nom_fichier,
            "nombre_pages": len(pages),
            "pages": pages
        }

        with open(chemin_sortie, "w", encoding="utf-8") as f:
            json.dump(resultat, f, ensure_ascii=False, indent=2)

        print(f"     ✅ {len(pages)} pages extraites → {nom_sortie}")

    print(f"\n🎉 Extraction terminée ! Résultats dans : {DOSSIER_SORTIE}")


if __name__ == "__main__":
    traiter_tous_les_pdfs()
