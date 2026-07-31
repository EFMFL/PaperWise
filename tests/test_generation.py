import os
import sys
import types
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import src.generation as generation


class GenerationFallbackTest(unittest.TestCase):
    def test_generer_reponse_fallback_when_model_call_fails(self):
        fake_retrieval = types.SimpleNamespace(
            rechercher=lambda question, nb_resultats=5: [
                {"texte": "Règlement intérieur applicable aux apprenants du Groupe OMNES Education.", "source": "Règlement intérieur.pdf", "page": 1, "score": 0.91}
            ]
        )
        sys.modules["src.retrieval"] = fake_retrieval
        generation._obtenir_modele = lambda: "fake-model"
        generation.ollama.chat = lambda **kwargs: (_ for _ in ()).throw(Exception("boom"))

        resultat = generation.generer_reponse("Quelles sont les règles ?", nb_chunks=1)

        self.assertIn("reponse", resultat)
        self.assertTrue(resultat["reponse"])
        self.assertEqual(resultat["sources"][0]["source"], "Règlement intérieur.pdf")


if __name__ == "__main__":
    unittest.main()
