import dspy

class EmailComposer(dspy.Module):
    """Compose a professional email to a hiring manager based on the evaluation summary and candidate status."""
    
    def __init__(self):
        super().__init__()
        self.compose = dspy.ChainOfThought("evaluation_summary, candidate_status -> email_text")
    
    def forward(self, evaluation_summary, candidate_status):
        return self.compose(evaluation_summary=evaluation_summary, candidate_status=candidate_status)