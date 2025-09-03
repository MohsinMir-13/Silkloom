import dspy

class EvaluateCandidateFit(dspy.Signature):
    analysis_result: str = dspy.InputField()
    job_criteria: str = dspy.InputField()
    evaluation_summary: str = dspy.OutputField(desc="Evaluation summary based on criteria")
"""""
class EvaluateJobDescription(dspy.Signature):
    job_description: str = dspy.InputField()
    evaluation_result: str = dspy.OutputField(desc="Evaluation of job description for clarity and completeness")    
class EvaluateCandidateCV(dspy.Signature):
    extracted_cv_info: str = dspy.InputField()
    evaluation_result: str = dspy.OutputField(desc="Evaluation of candidate CV for relevance and completeness")     
class EvaluateCommunicationHistory(dspy.Signature):
    communication_history: str = dspy.InputField()
    evaluation_result: str = dspy.OutputField(desc="Evaluation of communication history for relevance and clarity")
class EvaluateCandidateStatus(dspy.Signature):
    candidate_status: str = dspy.InputField()
    evaluation_result: str = dspy.OutputField(desc="Evaluation of candidate status for clarity and relevance")
class EvaluateContextualSummary(dspy.Signature):
    synthesized_context: str = dspy.InputField()
    evaluation_result: str = dspy.OutputField(desc="Evaluation of synthesized context for relevance and clarity")
class EvaluateCandidateProfile(dspy.Signature):
    candidate_info: str = dspy.InputField()
    job_info: str = dspy.InputField()
    communication_history: str = dspy.InputField(default="")
    evaluation_result: str = dspy.OutputField(desc="Evaluation of candidate profile based on job requirements and communication history")
class EvaluateCandidate(dspy.Signature):
    candidate_cv: str = dspy.InputField()
    job_description: str = dspy.InputField()
    candidate_status: str = dspy.InputField()
    evaluation_summary: str = dspy.OutputField(desc="Overall evaluation of candidate fit for the job based on CV, job description, and status")
class EvaluateCandidateEmail(dspy.Signature):
    evaluation_summary: str = dspy.InputField()
    candidate_status: str = dspy.InputField()
    email_text: str = dspy.OutputField(desc="Email text to candidate based on evaluation summary and status")
class EvaluateCandidateReport(dspy.Signature):
    evaluation_summary: str = dspy.InputField()
    report_text: str = dspy.OutputField(desc="Report text summarizing candidate evaluation")
"""