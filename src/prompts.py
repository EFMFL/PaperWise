def construire_prompt(question, chunks_trouves):
    """
    Construit le prompt complet à envoyer au modèle.

    - question       : la question posée par l'utilisateur
    - chunks_trouves : liste de dictionnaires avec 'texte', 'source', 'page'
    """

    contexte = ""
    for i, chunk in enumerate(chunks_trouves):
        contexte += f"""
[Source {i+1}] Article : {chunk['source']} — Page {chunk['page']}
{chunk['texte']}
---"""

    prompt = f"""Tu es un assistant scientifique expert. Tu aides des étudiants à comprendre des articles académiques.

RÈGLES IMPORTANTES que tu dois TOUJOURS respecter :
1. Tu réponds UNIQUEMENT en te basant sur les extraits fournis ci-dessous.
2. Pour chaque affirmation que tu fais, tu cites la source entre crochets : [Source 1], [Source 2], etc.
3. Tu rédiges des paragraphes clairs et bien structurés, comme dans un article scientifique.
4. Si la réponse ne se trouve pas dans les extraits, tu réponds exactement : "Je ne trouve pas la réponse à cette question dans les documents fournis."
5. Tu ne réponds JAMAIS avec des informations que tu as inventées ou mémorisées.

EXTRAITS DES ARTICLES SCIENTIFIQUES :
{contexte}

QUESTION DE L'UTILISATEUR :
{question}

RÉPONSE (en français, avec citations des sources) :"""

    return prompt


def construire_prompt_resume(chunks_trouves, nom_article):
    """
    Prompt spécial pour résumer un article entier.
    """
    contexte = "\n---\n".join([c['texte'] for c in chunks_trouves])

    prompt = f"""Tu es un assistant scientifique. Voici des extraits de l'article \"{nom_article}\".

Rédige un résumé structuré de cet article en 3 parties :
1. **Problématique** : Quel problème cet article cherche-t-il à résoudre ?
2. **Méthodes** : Quelles approches ou techniques sont utilisées ?
3. **Conclusions** : Quels sont les résultats et conclusions principaux ?

Cite toujours les extraits utilisés avec [Extrait X].

EXTRAITS :
{contexte}

RÉSUMÉ STRUCTURÉ :"""

    return prompt
