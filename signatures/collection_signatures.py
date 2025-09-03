import dspy

class CollectJobDescription(dspy.Signature):
    job_description: str = dspy.InputField()
    extracted_info: str = dspy.OutputField(desc="Structured info extracted from job description")

class CollectCandidateCV(dspy.Signature):
    cv_text: str = dspy.InputField()
    extracted_info: str = dspy.OutputField(desc="Structured info extracted from candidate CV")
