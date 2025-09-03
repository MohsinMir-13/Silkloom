import logging
from preprocessing.data_pipeline import load_and_process_file
from optimization.compile_agents import compile_all_agents

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SkilloomPipeline:
    def __init__(self):
        # Initialize and compile DSPy agents (assume dspy is already configured)
    # No get_dspy_params needed
        self.agents = compile_all_agents()
        logger.info("Agents compiled and pipeline initialized")

    def run_single_candidate(self, candidate_cv_path, job_description_path, communication_history=""):
        # Load and preprocess input files
        candidate_text = load_and_process_file(candidate_cv_path)
        job_text = load_and_process_file(job_description_path)

        logger.info("Data loaded and preprocessed")

        # Run Info Collectors
        job_info = self.agents["info_collector_job"](job_description=job_text)
        cv_info = self.agents["info_collector_cv"](cv_text=candidate_text)

        # Run CV Analyzer
        analysis = self.agents["cv_analyzer"](extracted_cv_info=cv_info["extracted_info"])

        # Context synthesis
        context = self.agents["context_synthesizer"](
            candidate_info=cv_info["extracted_info"],
            job_info=job_info["extracted_info"],
            communication_history=communication_history
        )

        # Candidate evaluation
        evaluation = self.agents["evaluator"](
            analysis_result=analysis["analysis_result"],
            job_criteria=job_info["extracted_info"]
        )

        # Compose email
        email = self.agents["email_composer"](
            evaluation_summary=evaluation["evaluation_summary"],
            candidate_status="Shortlisted"
        )

        # Generate report
        report = self.agents["report_generator"](evaluation_summary=evaluation["evaluation_summary"])

        logger.info("Pipeline run completed")

        return {
            "email": email["email_text"],
            "report": report["report_text"],
            "evaluation_summary": evaluation["evaluation_summary"],
            "context": context,
        }

    def run_batch(self, candidate_files, job_description_path, communication_histories=None):
        """
        Process multiple candidates in batch mode.
        :param candidate_files: list of paths to candidate CVs
        :param job_description_path: path to job description
        :param communication_histories: list of communication history strings (optional)
        :return: list of dicts with pipeline outputs per candidate
        """
        results = []
        if communication_histories is None:
            communication_histories = [""] * len(candidate_files)

        for cv_path, comm_hist in zip(candidate_files, communication_histories):
            logger.info(f"Processing candidate CV: {cv_path}")
            try:
                result = self.run_single_candidate(cv_path, job_description_path, comm_hist)
                results.append(result)
            except Exception as e:
                logger.error(f"Failed processing {cv_path}: {e}")
                results.append({"error": str(e), "cv_path": cv_path})

        return results


if __name__ == "__main__":
    pipeline = SkilloomPipeline()

    # Example single run
    candidate_cv = "data/cvs/sample_candidate.pdf"
    job_desc = "data/job_descriptions/sample_job.txt"

    output = pipeline.run_single_candidate(candidate_cv, job_desc)
    print("\n=== Email ===\n", output["email"])
    print("\n=== Report ===\n", output["report"])
