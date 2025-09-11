from verifier import Verifier
from data import Data


class PointSetVerifier(Verifier):
    def __init__(self):
        super().__init__()

    def verify(self, data: Data, test_answer: str) -> bool:
        try:
            extracted_answer = self.extract_answer(test_answer)
            ground_truth = data.answer

            extracted_normalized = self._normalize_classification(extracted_answer)
            ground_truth_normalized = self._normalize_classification(ground_truth)

            return extracted_normalized == ground_truth_normalized

        except Exception as e:
            print(f"Error in verification: {e}")
            return False

    def extract_answer(self, test_solution: str) -> str:
        if not test_solution:
            return ""

        test_solution_lower = test_solution.lower()

        if any(word in test_solution_lower for word in ["внутрен", "internal"]):
            return "internal"
        elif any(word in test_solution_lower for word in ["гранич", "boundary"]):
            return "boundary"
        elif any(word in test_solution_lower for word in ["внешн", "external"]):
            return "external"
        else:
            lines = test_solution.split('\n')
            for line in lines:
                line_lower = line.lower()
                if "ответ:" in line_lower or "answer:" in line_lower:
                    if any(word in line_lower for word in ["внутрен", "internal"]):
                        return "internal"
                    elif any(word in line_lower for word in ["гранич", "boundary"]):
                        return "boundary"
                    elif any(word in line_lower for word in ["внешн", "external"]):
                        return "external"

            return ""

    def _normalize_classification(self, classification: str) -> str:
        classification_lower = classification.lower()

        if any(word in classification_lower for word in ["внутрен", "internal"]):
            return "internal"
        elif any(word in classification_lower for word in ["гранич", "boundary", "поверхност"]):
            return "boundary"
        elif any(word in classification_lower for word in ["внешн", "external"]):
            return "external"
        else:
            return classification_lower