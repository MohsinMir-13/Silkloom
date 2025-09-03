import dspy
from signatures.analysis_signatures import AnalyzeCandidateCV

class CVAnalyzer(dspy.Module):
    def __init__(self):
        super().__init__()
        self.predict = dspy.Predict(AnalyzeCandidateCV)

    def forward(self, extracted_cv_info: str):
        prompt = f"""
You are a skilled HR specialist. Analyze the candidate information extracted from their CV below.
Provide a clear summary of:
- Key strengths
- Weaknesses or gaps
- Relevant skills and experiences
- Overall suitability for the role

Candidate Information:
{extracted_cv_info}

Analysis:
"""
        return self.predict(extracted_cv_info=extracted_cv_info, prompt=prompt)
