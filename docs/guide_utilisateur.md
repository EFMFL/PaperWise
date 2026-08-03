# Guide utilisateur — PaperWise

PaperWise vous permet de **poser des questions à vos articles PDF** et d'obtenir
des réponses générées localement, avec les sources exactes (article + page).

## Vue d'ensemble de l'interface

L'interface se compose de deux zones :

- **La barre latérale (à gauche)** : gestion des documents (dépôt des PDF et indexation).
- **La zone principale** : le chat où vous posez vos questions.

## 1. Déposer vos articles PDF

1. Dans la barre latérale, cliquez sur **« Browse files »** (ou glissez-déposez vos fichiers).
2. Sélectionnez un ou plusieurs fichiers PDF.
3. Un message de confirmation s'affiche : vos fichiers sont enregistrés dans `data/pdfs/`.

> ⚠️ Les PDF doivent contenir du **texte sélectionnable**. Les scans (images de pages)
> ne peuvent pas être lus.

## 2. Indexer les documents

Cliquez sur le bouton **« 🔄 Lancer l'indexation »**. Le système effectue 3 étapes :

1. **Extraction** — le texte de chaque page est extrait des PDF.
2. **Découpage** — le texte est découpé en passages (« chunks »).
3. **Indexation** — chaque passage est transformé en vecteur et stocké dans la base.

> ⏳ Cette étape peut prendre quelques minutes selon le nombre de documents.
> Elle n'est nécessaire **qu'une seule fois par document** : la base est
> sauvegardée sur le disque (`data/chroma_db/`).

Le compteur de la barre latérale indique combien de passages sont indexés.

## 3. Poser une question

Tapez votre question dans la zone de saisie en bas de l'écran et appuyez sur **Entrée**.

Exemples de questions :

- *« Quelles sont les conclusions principales de l'article ? »*
- *« Quelles méthodes sont utilisées dans cette étude ? »*
- *« Que dit le document au sujet de … ? »*

## 4. Lire la réponse et vérifier les sources

La réponse apparaît dans le chat. Sous chaque réponse, un panneau
**« 📌 Sources utilisées »** liste les passages sur lesquels la réponse s'appuie :

- le **nom du fichier** PDF source ;
- le **numéro de page** ;
- le **score de pertinence** (plus il est proche de 1, plus le passage est pertinent) ;
- un **extrait** du passage.

> 💡 Vérifiez toujours les sources : le système est conçu pour ne répondre
> qu'à partir de vos documents, mais la lecture des passages cités reste la
> meilleure garantie.

## Questions fréquentes

**La réponse dit « Je ne trouve pas la réponse dans les documents fournis. »**
C'est normal : le système refuse d'inventer. Reformulez votre question ou
vérifiez que le bon document est indexé.

**La génération est très lente.**
La vitesse dépend de votre machine et du modèle Ollama utilisé. Essayez un
modèle plus léger (voir le guide d'installation).

**Je veux repartir de zéro.**
Supprimez le dossier `data/chroma_db/` puis relancez l'indexation.
