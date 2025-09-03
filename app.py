import config  # Ensure LM is configured before pipeline import
import streamlit as st
import tempfile
import os
from pipeline import SkilloomPipeline

def main():
    st.set_page_config(page_title="Skilloom CV/Job Evaluator", layout="wide")
    st.title("Skilloom CV & Job Description Evaluator")
    st.markdown("""
    Upload or paste CVs and job descriptions. Choose single or batch mode. Get results instantly!
    """)

    mode = st.radio("Choose mode", ["Single CV", "Batch CVs"])

    # Job description input
    st.subheader("Job Description")
    job_input_type = st.radio("Input method for job description", ["Paste text", "Upload file"])
    if job_input_type == "Paste text":
        job_text = st.text_area("Paste job description here", height=150)
        job_path = None
    else:
        job_file = st.file_uploader("Upload job description (TXT)", type=["txt"], key="job")
        job_text = None
        job_path = None
        if job_file:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as tmp:
                tmp.write(job_file.read())
                job_path = tmp.name

    # CV input
    st.subheader("CV(s)")
    if mode == "Single CV":
        cv_input_type = st.radio("Input method for CV", ["Paste text", "Upload file"])
        if cv_input_type == "Paste text":
            cv_text = st.text_area("Paste CV here", height=200)
            cv_path = None
        else:
            cv_file = st.file_uploader("Upload CV (PDF or TXT)", type=["pdf", "txt"], key="cv")
            cv_text = None
            cv_path = None
            if cv_file:
                with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(cv_file.name)[-1]) as tmp:
                    tmp.write(cv_file.read())
                    cv_path = tmp.name
    else:
        cv_files = st.file_uploader("Upload multiple CVs (PDF or TXT)", type=["pdf", "txt"], accept_multiple_files=True, key="cvs")
        pasted_cvs = st.text_area("Or paste multiple CVs, separated by \n---CV---\n", height=200)
        cv_paths = []
        if cv_files:
            for cv in cv_files:
                with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(cv.name)[-1]) as tmp:
                    tmp.write(cv.read())
                    cv_paths.append(tmp.name)
        if pasted_cvs.strip():
            for idx, cvtxt in enumerate(pasted_cvs.split("---CV---")):
                with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as tmp:
                    tmp.write(cvtxt.strip().encode())
                    cv_paths.append(tmp.name)

    if st.button("Run Evaluation"):
        with st.spinner("Processing..."):
            pipeline = SkilloomPipeline()
            # Prepare job file
            if job_text and not job_path:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as tmp:
                    tmp.write(job_text.encode())
                    job_path = tmp.name
            if mode == "Single CV":
                # Prepare CV file
                if cv_text and not cv_path:
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as tmp:
                        tmp.write(cv_text.encode())
                        cv_path = tmp.name
                if not job_path or not cv_path:
                    st.error("Please provide both job description and CV.")
                    return
                result = pipeline.run_single_candidate(cv_path, job_path)
                st.subheader("Email")
                st.code(result["email"], language="text")
                st.download_button("Download Email", result["email"], file_name="email.txt")
                st.subheader("Report")
                st.code(result["report"], language="text")
                st.download_button("Download Report", result["report"], file_name="report.txt")
            else:
                if not job_path or not cv_paths:
                    st.error("Please provide job description and at least one CV.")
                    return
                results = pipeline.run_batch(cv_paths, job_path)
                for i, result in enumerate(results):
                    st.markdown(f"### Candidate {i+1}")
                    if 'error' in result:
                        st.error(f"Error: {result['error']}")
                        continue
                    st.markdown("**Email:**")
                    st.code(result["email"], language="text")
                    st.download_button(f"Download Email {i+1}", result["email"], file_name=f"email_candidate_{i+1}.txt")
                    st.markdown("**Report:**")
                    st.code(result["report"], language="text")
                    st.download_button(f"Download Report {i+1}", result["report"], file_name=f"report_candidate_{i+1}.txt")

if __name__ == "__main__":
    main()

