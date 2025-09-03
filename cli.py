
import glob
import os
import config  # Ensure LM is configured
from pipeline import SkilloomPipeline

def prompt_text_input(prompt, multiline=False):
    print(prompt)
    if multiline:
        print("(Enter your text. Finish with a single line containing only 'END')")
        lines = []
        while True:
            line = input()
            if line.strip() == 'END':
                break
            lines.append(line)
        return '\n'.join(lines)
    else:
        return input()

def interactive_cli():
    print("\n=== Skilloom Interactive CLI ===")
    print("Choose mode:")
    print("1. Single CV evaluation")
    print("2. Batch CV evaluation")
    mode = input("Enter 1 or 2: ").strip()

    # Job description input
    print("\nJob Description Input:")
    print("a. Paste job description text")
    print("b. Provide job description file path")
    job_choice = input("Choose a or b: ").strip().lower()
    if job_choice == 'a':
        job_text = prompt_text_input("Paste job description:", multiline=True)
        with open("/tmp/skilloom_job.txt", "w") as f:
            f.write(job_text)
        job_path = "/tmp/skilloom_job.txt"
    else:
        job_path = input("Enter job description file path: ").strip()
        if not os.path.isfile(job_path):
            print("File not found.")
            return

    if mode == '1':
        print("\nCV Input:")
        print("a. Paste CV text")
        print("b. Provide CV file path")
        cv_choice = input("Choose a or b: ").strip().lower()
        if cv_choice == 'a':
            cv_text = prompt_text_input("Paste CV:", multiline=True)
            with open("/tmp/skilloom_cv.txt", "w") as f:
                f.write(cv_text)
            cv_path = "/tmp/skilloom_cv.txt"
        else:
            cv_path = input("Enter CV file path: ").strip()
            if not os.path.isfile(cv_path):
                print("File not found.")
                return
        pipeline = SkilloomPipeline()
        result = pipeline.run_single_candidate(cv_path, job_path)
        print("\n=== Email ===\n" + result["email"])
        print("\n=== Report ===\n" + result["report"])
    else:
        print("\nBatch CV Input:")
        print("a. Paste multiple CVs (one after another, type END to finish each, and ENDALL to finish batch)")
        print("b. Provide CV file paths or glob pattern")
        batch_choice = input("Choose a or b: ").strip().lower()
        cv_paths = []
        if batch_choice == 'a':
            idx = 1
            while True:
                print(f"Paste CV #{idx} (type END to finish this CV, ENDALL to finish batch):")
                lines = []
                while True:
                    line = input()
                    if line.strip() == 'ENDALL':
                        break
                    if line.strip() == 'END':
                        break
                    lines.append(line)
                if line.strip() == 'ENDALL':
                    break
                cv_file = f"/tmp/skilloom_cv_{idx}.txt"
                with open(cv_file, "w") as f:
                    f.write('\n'.join(lines))
                cv_paths.append(cv_file)
                idx += 1
        else:
            pattern = input("Enter CV file paths or glob pattern (space separated): ").strip()
            for p in pattern.split():
                cv_paths.extend(glob.glob(p))
        if not cv_paths:
            print("No CVs provided.")
            return
        pipeline = SkilloomPipeline()
        results = pipeline.run_batch(cv_paths, job_path)
        for i, result in enumerate(results):
            print(f"\n=== Candidate {i+1} ===")
            if 'error' in result:
                print(f"Error: {result['error']}")
                continue
            print("--- Email ---\n" + result['email'])
            print("--- Report ---\n" + result['report'])

if __name__ == "__main__":
    interactive_cli()

def main():
    parser = argparse.ArgumentParser(description="Skilloom CLI: Evaluate CVs against a job description.")
    parser.add_argument('--job', type=str, required=True, help='Path to job description (TXT)')
    parser.add_argument('--cvs', type=str, nargs='+', required=True, help='Paths to CV files (PDF or TXT, space separated, or glob pattern)')
    parser.add_argument('--output', type=str, default=None, help='Directory to save results (optional)')
    args = parser.parse_args()

    # Expand glob patterns for CVs
    cv_files = []
    for pattern in args.cvs:
        cv_files.extend(glob.glob(pattern))
    cv_files = list(set(cv_files))  # Remove duplicates
    if not cv_files:
        print("No CV files found.")
        return
    if not os.path.isfile(args.job):
        print(f"Job description file not found: {args.job}")
        return

    print(f"Processing {len(cv_files)} CV(s) against job: {args.job}")
    pipeline = SkilloomPipeline()
    results = pipeline.run_batch(cv_files, args.job)

    for i, result in enumerate(results):
        print(f"\n=== Candidate {i+1} ===")
        if 'error' in result:
            print(f"Error: {result['error']}")
            continue
        print("--- Email ---\n" + result['email'])
        print("--- Report ---\n" + result['report'])
        if args.output:
            os.makedirs(args.output, exist_ok=True)
            with open(os.path.join(args.output, f"email_candidate_{i+1}.txt"), 'w') as f:
                f.write(result['email'])
            with open(os.path.join(args.output, f"report_candidate_{i+1}.txt"), 'w') as f:
                f.write(result['report'])
    if args.output:
        print(f"\nResults saved to: {args.output}")

if __name__ == "__main__":
    main()
