from typing import ClassVar, List, Tuple
from dspy import Signature

class ComposeEmail(Signature):
    inputs: ClassVar[List[Tuple[str, type]]] = [
        ("evaluation_summary", str),
        ("candidate_status", str),
    ]

    outputs: ClassVar[List[Tuple[str, type]]] = [
        ("email_text", str),
    ]

    template: ClassVar[str] = """
You are an AI assistant tasked with composing a professional email to a hiring manager
based on the evaluation summary and candidate status.

Evaluation Summary:
{evaluation_summary}

Candidate Status: {candidate_status}

Please generate a polite and clear email to the hiring manager.
"""

    def run(self, evaluation_summary: str, candidate_status: str) -> dict:
        prompt = self.template.format(
            evaluation_summary=evaluation_summary,
            candidate_status=candidate_status,
        )
        result = self.predict(prompt=prompt)
        return {"email_text": result}
