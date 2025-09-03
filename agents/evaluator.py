import dspy
from signatures.evaluation_signatures import EvaluateCandidateFit

class CandidateEvaluator(dspy.Module):
    def __init__(self):
        super().__init__()
        self.predict = dspy.Predict(EvaluateCandidateFit)

    def forward(self, analysis_result: str, job_criteria: str):
        prompt = f"""You are an experienced recruiter. Based on the candidate analysis and the job criteria, provide a concise evaluation summary highlighting:

- Candidate’s overall fit
- Key strengths matching the criteria
- Any gaps or weaknesses
- Recommendations for next steps

Job Criteria:
{job_criteria}

Candidate Analysis:
{analysis_result}

Evaluation Summary:
"""
        return self.predict(analysis_result=analysis_result, job_criteria=job_criteria, prompt=prompt)
#         return self.predict(analysis_result=analysis_result, job_criteria=job_criteria, prompt=prompt)
