import dspy

class ReportGenerator(dspy.Module):
    """Generate a structured report for the hiring manager based on candidate evaluation."""
    
    def __init__(self):
        super().__init__()
        self.generate = dspy.ChainOfThought("evaluation_summary -> report_text")
    
    def forward(self, evaluation_summary):
        return self.generate(evaluation_summary=evaluation_summary)