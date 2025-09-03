import dspy
from signatures.context_synthesizer_signatures import SynthesizeContext

class ContextSynthesizer(dspy.Module):
    def __init__(self):
        super().__init__()
        self.predict = dspy.Predict(SynthesizeContext)

    def forward(self, candidate_info: str, job_info: str, communication_history: str = ""):
        prompt = f"""Given the following data:

Candidate Info:
{candidate_info}

Job Info:
{job_info}

Communication History:
{communication_history}

Please synthesize a concise, relevant context summary combining these details, highlighting key points for hiring decisions.

Synthesized Context:
"""
        return self.predict(candidate_info=candidate_info, job_info=job_info, communication_history=communication_history, prompt=prompt)
