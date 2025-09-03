def keyword_coverage_score(output_text: str, expected_keywords: list) -> float:
    """
    Computes the percentage of expected keywords present in the output text.
    """
    count = sum(1 for kw in expected_keywords if kw.lower() in output_text.lower())
    return count / len(expected_keywords) if expected_keywords else 0.0

def length_score(output_text: str, min_len=50, max_len=300) -> float:
    """
    Score based on output text length falling within an expected range.
    """
    length = len(output_text)
    if length < min_len:
        return length / min_len
    elif length > max_len:
        return max_len / length
    return 1.0

def combined_score(output_text: str, expected_keywords: list) -> float:
    """
    Weighted combination of keyword coverage and length scores.
    """
    kw_score = keyword_coverage_score(output_text, expected_keywords)
    len_score = length_score(output_text)
    return 0.7 * kw_score + 0.3 * len_score
def email_tone_metric(email_text: str) -> float:
    """Evaluates the tone of an email based on predefined criteria.
    Returns a score between 0 and 1, where 1 indicates a positive tone.
    """
    positive_keywords = ["appreciate", "thank", "grateful", "pleased", "excited"]
    negative_keywords = ["unfortunately", "regret", "disappointed", "concerned"]

    positive_score = sum(1 for word in positive_keywords if word in email_text.lower())
    negative_score = sum(1 for word in negative_keywords if word in email_text.lower())

    total_keywords = len(positive_keywords) + len(negative_keywords)
    if total_keywords == 0:
        return 0.0

    return positive_score / total_keywords - negative_score / total_keywords        
def evaluation_completeness_metric(evaluation_text: str) -> float:
    """Evaluates the completeness of an evaluation based on the presence of key components.
    Returns a score between 0 and 1, where 1 indicates a complete evaluation.
    """
    required_components = ["strengths", "weaknesses", "skills", "experience", "recommendation"]
    present_components = sum(1 for component in required_components if component in evaluation_text.lower())
    
    return present_components / len(required_components) if required_components else 0.0    
def evaluation_relevance_metric(evaluation_text: str, job_description: str) -> float:
    """Evaluates the relevance of an evaluation based on its alignment with job requirements.
    Returns a score between 0 and 1, where 1 indicates high relevance.
    """
    job_keywords = set(job_description.lower().split())
    evaluation_keywords = set(evaluation_text.lower().split())
    
    relevant_keywords = job_keywords.intersection(evaluation_keywords)
    
    return len(relevant_keywords) / len(job_keywords) if job_keywords else 0.0
def evaluation_clarity_metric(evaluation_text: str) -> float:
    """Evaluates the clarity of an evaluation based on sentence structure and readability.
    Returns a score between 0 and 1, where 1 indicates high clarity.
    """
    sentences = evaluation_text.split('.')
    clear_sentences = sum(1 for sentence in sentences if len(sentence.split()) > 5)  # Simple heuristic
    
    return clear_sentences / len(sentences) if sentences else 0.0
def evaluation_consistency_metric(evaluation_text: str, previous_evaluations: list) -> float:
    """Evaluates the consistency of an evaluation with previous evaluations.
    Returns a score between 0 and 1, where 1 indicates high consistency.
    """
    if not previous_evaluations:
        return 1.0  # No previous evaluations to compare against
    
    current_keywords = set(evaluation_text.lower().split())
    consistency_scores = []
    
    for prev_eval in previous_evaluations:
        prev_keywords = set(prev_eval.lower().split())
        common_keywords = current_keywords.intersection(prev_keywords)
        consistency_scores.append(len(common_keywords) / len(prev_keywords) if prev_keywords else 0.0)
    
    return sum(consistency_scores) / len(consistency_scores) if consistency_scores else 0.0
def evaluation_timeliness_metric(evaluation_date: str, current_date: str) -> float:
    """Evaluates the timeliness of an evaluation based on the date it was created.
    Returns a score between 0 and 1, where 1 indicates a recent evaluation.
    """
    from datetime import datetime
    
    eval_date = datetime.strptime(evaluation_date, "%Y-%m-%d")
    curr_date = datetime.strptime(current_date, "%Y-%m-%d")
    
    days_difference = (curr_date - eval_date).days
    if days_difference < 30:
        return 1.0  # Recent evaluation
    elif days_difference < 90:
        return 0.5  # Moderately recent
    else:
        return 0.0  # Old evaluation
def evaluation_actionability_metric(evaluation_text: str) -> float:
    """Evaluates the actionability of an evaluation based on clear recommendations.
    Returns a score between 0 and 1, where 1 indicates high actionability.
    """
    actionable_phrases = ["recommend", "suggest", "advise", "action", "next steps"]
    actionable_count = sum(1 for phrase in actionable_phrases if phrase in evaluation_text.lower())
    
    return actionable_count / len(actionable_phrases) if actionable_phrases else 0.0
def evaluation_comprehensiveness_metric(evaluation_text: str) -> float:
    """Evaluates the comprehensiveness of an evaluation based on coverage of key areas.
    Returns a score between 0 and 1, where 1 indicates high comprehensiveness.
    """
    key_areas = ["skills", "experience", "education", "cultural fit", "recommendation"]
    covered_areas = sum(1 for area in key_areas if area in evaluation_text.lower())
    
    return covered_areas / len(key_areas) if key_areas else 0.0
def evaluation_objectivity_metric(evaluation_text: str) -> float:   
    """Evaluates the objectivity of an evaluation based on neutral language and absence of bias.
    Returns a score between 0 and 1, where 1 indicates high objectivity.
    """
    subjective_phrases = ["I think", "I feel", "in my opinion", "believe"]
    objective_phrases = ["data shows", "evidence suggests", "analysis indicates"]
    
    subjective_count = sum(1 for phrase in subjective_phrases if phrase in evaluation_text.lower())
    objective_count = sum(1 for phrase in objective_phrases if phrase in evaluation_text.lower())
    
    return (objective_count - subjective_count) / (objective_count + subjective_count) if (objective_count + subjective_count) > 0 else 0.0     
