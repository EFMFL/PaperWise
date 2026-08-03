"""
eval_retrieval.py
-------------------
Évalue la qualité du retrieval (recherche vectorielle) avec un petit
jeu de questions-réponses dont on connaît la page attendue.

Principe :
- On définit une liste de questions avec la page où se trouve la
  vraie réponse dans le PDF (à adapter selon ton propre article).
- Pour chaque question, on regarde si cette page apparaît dans le
  top_k des résultats retournés par la recherche.
- On calcule un taux de rappel global : (questions réussies / total)
"""

from vector_store import VectorStore


# Jeu de test : (question, page(s) attendue(s) où se trouve la réponse)
# À ADAPTER selon TON propre article PDF !
TEST_QUESTIONS = [
    {
        "question": "What is Spiral Jetty and where is it located?",
        "expected_pages": [1, 2],
    },
    {
        "question": "What IPCC SSP scenarios are used in the climate forecast?",
        "expected_pages": [5, 6],
    },
    {
        "question": "What happens to the lake elevation by 2050?",
        "expected_pages": [6, 8],
    },
    {
        "question": "What generative model architecture is used for visual synthesis?",
        "expected_pages": [9],
    },
    {
        "question": "What ethical considerations are discussed about generating images of cultural heritage?",
        "expected_pages": [10, 11],
    },
]


def evaluate_retrieval(store: VectorStore, top_k: int = 3) -> dict:
    """
    Évalue le retrieval sur le jeu de test.

    Returns:
        dict avec le détail par question + le taux de rappel global.
    """
    results_detail = []
    successes = 0

    for test_case in TEST_QUESTIONS:
        question = test_case["question"]
        expected_pages = set(test_case["expected_pages"])

        search_results = store.search(question, top_k=top_k)
        retrieved_pages = [r["page_number"] for r in search_results]

        # Succès si au moins une page attendue est dans les résultats retournés
        found = any(page in expected_pages for page in retrieved_pages)
        if found:
            successes += 1

        results_detail.append({
            "question": question,
            "expected_pages": sorted(expected_pages),
            "retrieved_pages": retrieved_pages,
            "success": found,
        })

    recall = successes / len(TEST_QUESTIONS)

    return {
        "recall": recall,
        "successes": successes,
        "total": len(TEST_QUESTIONS),
        "details": results_detail,
    }


def print_evaluation_report(evaluation: dict) -> None:
    """Affiche un rapport lisible de l'évaluation."""
    print("=" * 60)
    print(f"RAPPORT D'ÉVALUATION DU RETRIEVAL")
    print("=" * 60)

    for detail in evaluation["details"]:
        status = "✅" if detail["success"] else "❌"
        print(f"\n{status} Question : {detail['question']}")
        print(f"   Pages attendues  : {detail['expected_pages']}")
        print(f"   Pages retrouvées : {detail['retrieved_pages']}")

    print("\n" + "=" * 60)
    print(f"RAPPEL GLOBAL : {evaluation['successes']}/{evaluation['total']} "
          f"({evaluation['recall'] * 100:.0f}%)")
    print("=" * 60)


if __name__ == "__main__":
    store = VectorStore()

    if store.count() == 0:
        print("⚠️  Base vectorielle vide. Lance d'abord vector_store.py pour indexer tes PDF.")
    else:
        print(f"Base vectorielle : {store.count()} chunks indexés.\n")

        evaluation = evaluate_retrieval(store, top_k=5)
        print_evaluation_report(evaluation)
