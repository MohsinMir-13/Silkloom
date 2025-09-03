def main():
    try:
        # Configuration
        AUTO_EMAIL = os.getenv("AUTO_EMAIL", "false").lower() == "true"  # Set AUTO_EMAIL=true to enable
        
        # Load OpenAI API key
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY is not set in environment variables")
        logger.info("OpenAI API key loaded from environment variable")

        # Configure DSPy
        lm = dspy.LM(model='openai/gpt-3.5-turbo', api_key=api_key)
        dspy.configure(lm=lm)
        logger.info("DSPy configured with OpenAI language model")

        # Compile agents
        agents = compile_all_agents()

        # Load job description (single file for all CVs)
        job_description_path = "data/job_descriptions/sample_job.txt"
        job_text = load_and_process_file(job_description_path)
        job_info = agents["info_collector_job"](job_description=job_text)

        # Find all CV files (supports PDF and TXT)
        cv_files = []
        cv_files.extend(glob.glob("data/cvs/*.pdf"))
        cv_files.extend(glob.glob("data/cvs/*.txt"))
        
        # Filter out non-CV files and system files
        cv_files = [f for f in cv_files if not os.path.basename(f).startswith('.') and 'sample_candidate' in f]
        
        if not cv_files:
            logger.error("No CV files found in data/cvs/")
            return
            
        logger.info(f"Found {len(cv_files)} CV files to process")
        if AUTO_EMAIL:
            logger.info("Automatic email sending is ENABLED")
        else:
            logger.info("Automatic email sending is DISABLED (set AUTO_EMAIL=true to enable)")

        # Process each CV
        results = []
        for i, cv_path in enumerate(cv_files, 1):
            logger.info(f"Processing CV {i}/{len(cv_files)}: {os.path.basename(cv_path)}")
            result = process_single_cv(agents, cv_path, job_text, job_info, auto_email=AUTO_EMAIL)
            if result:
                results.append(result)

        # Create output directory
        os.makedirs("output", exist_ok=True)

        # Save batch results
        with open("output/batch_results.txt", "w") as f:
            f.write(f"BATCH CV EVALUATION RESULTS\n")
            f.write(f"Job Position: Senior Software Engineer\n")
            f.write(f"Total CVs Processed: {len(results)}\n")
            f.write(f"Auto Email Enabled: {AUTO_EMAIL}\n")
            f.write("="*50 + "\n\n")
            
            for result in results:
                f.write(f"CANDIDATE: {result['candidate_name']}\n")
                f.write(f"File: {result['filename']}\n")
                if AUTO_EMAIL:
                    f.write(f"Email Sent: {'Yes' if result['email_sent'] else 'Failed'}\n")
                f.write("-" * 30 + "\n")
                f.write("EMAIL:\n")
                f.write(result['email'].email_text + "\n\n")
                f.write("REPORT:\n")
                f.write(result['report'].report_text + "\n\n")
                f.write("="*50 + "\n\n")

        # Save individual files for each candidate
        for result in results:
            safe_filename = result['filename'].replace('.', '_').replace('/', '_')
            
            # Save individual email
            with open(f"output/email_{safe_filename}.txt", "w") as f:
                f.write(result['email'].email_text)
            
            # Save individual report
            with open(f"output/report_{safe_filename}.txt", "w") as f:
                f.write(result['report'].report_text)

        logger.info(f"Pipeline completed successfully. Processed {len(results)} CVs.")
        logger.info("Results saved to output/ directory")

        # Print summary to terminal
        print(f"\n=== BATCH PROCESSING COMPLETE ===")
        print(f"Processed: {len(results)} CVs")
        print(f"Auto Email: {'Enabled' if AUTO_EMAIL else 'Disabled'}")
        if AUTO_EMAIL:
            emails_sent = sum(1 for r in results if r.get('email_sent', False))
            print(f"Emails Sent: {emails_sent}/{len(results)}")
        print(f"Results saved to: output/")
        print(f"Files created:")
        print(f"  - output/batch_results.txt (combined results)")
        for result in results:
            safe_name = result['filename'].replace('.', '_').replace('/', '_')
            print(f"  - output/email_{safe_name}.txt")
            print(f"  - output/report_{safe_name}.txt")

    except Exception as e:
        logger.error(f"Error in pipeline execution: {e}")