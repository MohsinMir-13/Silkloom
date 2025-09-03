import dspy
from signatures.collection_signatures import CollectJobDescription, CollectCandidateCV

class JobDescriptionCollector(dspy.Module):
    def __init__(self):
        super().__init__()
        self.predict = dspy.Predict(CollectJobDescription)

    def forward(self, job_description: str):
        prompt = f"""Extract key job requirements, responsibilities, and skills from the following job description. Present the information as clear bullet points:

{job_description}

Extracted Info:
"""
        return self.predict(job_description=job_description, prompt=prompt)

class CandidateCVCollector(dspy.Module):
    def __init__(self):
        super().__init__()
        self.predict = dspy.Predict(CollectCandidateCV)

    def forward(self, cv_text: str):
        prompt = f"""Extract key candidate details such as skills, experience, education, and certifications from this CV text. Summarize clearly:

{cv_text}

Extracted Info:
"""
        return self.predict(cv_text=cv_text, prompt=prompt)
