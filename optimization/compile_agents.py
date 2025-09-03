from agents.info_collector import JobDescriptionCollector, CandidateCVCollector
from agents.cv_analyzer import CVAnalyzer
from agents.evaluator import CandidateEvaluator
from agents.context_synthesizer import ContextSynthesizer
from agents.email_composer import EmailComposer
from agents.report_generator import ReportGenerator

def compile_all_agents():
    compiled_agents = {
        "info_collector_job": JobDescriptionCollector(),
        "info_collector_cv": CandidateCVCollector(),
        "cv_analyzer": CVAnalyzer(),
        "context_synthesizer": ContextSynthesizer(),
        "evaluator": CandidateEvaluator(),
        "email_composer": EmailComposer(),
        "report_generator": ReportGenerator(),
    }
    print("All agents instantiated successfully.")
    return compiled_agents

if __name__ == "__main__":
    agents = compile_all_agents()
    for name, agent in agents.items():
        print(f"{name} instantiated: {agent}")
