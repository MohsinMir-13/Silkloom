PROMPT_CONFIG = {
    "system_message": "You are an expert AI assistant specialized in recruitment and HR analytics.",
    "temperature": 0.3,
    "max_tokens": 512,
    "top_p": 1.0,
    "frequency_penalty": 0,
    "presence_penalty": 0,
}
TELEPROMPTER_CONFIG = {
    "prompt_template": """You are a skilled HR specialist. Analyze the candidate information extracted from their CV below.
Provide a clear summary of:
- Key strengths
- Weaknesses or gaps
- Relevant skills and experiences
- Overall suitability for the role
Candidate Information:
{extracted_cv_info}
Analysis:
""",
    "input_fields": ["extracted_cv_info"],
    "output_field": "analysis_result",
    "signature": "AnalyzeCandidateCV",
    "model": "gpt-4",
    "config": PROMPT_CONFIG,
}