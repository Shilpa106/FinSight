class AnswerMetrics:
    def score(
        self,
        actual_answer: str | None,
        expected_keywords: list[str],
    ) -> tuple[float, dict]:
        if not actual_answer:
            return 0.0, {
                "expected_keywords": expected_keywords,
                "matched_keywords": [],
            }

        if not expected_keywords:
            return 1.0, {
                "expected_keywords": [],
                "matched_keywords": [],
                "note": "No expected keywords provided.",
            }

        normalized_answer = actual_answer.lower()

        matched_keywords = [
            keyword
            for keyword in expected_keywords
            if keyword.lower() in normalized_answer
        ]

        score = len(matched_keywords) / len(expected_keywords)

        return score, {
            "expected_keywords": expected_keywords,
            "matched_keywords": matched_keywords,
        }