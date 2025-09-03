import dspy

class AnalyzeCandidateCV(dspy.Signature):
    extracted_cv_info: str = dspy.InputField()
    analysis_result: str = dspy.OutputField(desc="Analysis of candidate's strengths, weaknesses, and skills")
