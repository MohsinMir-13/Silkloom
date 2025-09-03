import dspy

class SynthesizeContext(dspy.Signature):
    candidate_info: str = dspy.InputField()
    job_info: str = dspy.InputField()
    communication_history: str = dspy.InputField(default="")
    synthesized_context: str = dspy.OutputField(desc="Synthesized contextual summary")
