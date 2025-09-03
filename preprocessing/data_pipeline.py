import os
import re
import pandas as pd
import docx
import PyPDF2

def extract_text_from_pdf(file_path):
    text = ""
    with open(file_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

def extract_text_from_docx(file_path):
    doc = docx.Document(file_path)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return "\n".join(full_text)

def extract_text_from_xlsx(file_path):
    df = pd.read_excel(file_path)
    # Flatten all cells to a single string (customize per your data)
    text = "\n".join(df.astype(str).fillna("").values.flatten())
    return text

def clean_text(text):
    # Basic cleaning: remove multiple spaces, newlines, tabs
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    return text

def load_and_process_file(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    if ext in ['.pdf']:
        raw_text = extract_text_from_pdf(file_path)
    elif ext in ['.docx']:
        raw_text = extract_text_from_docx(file_path)
    elif ext in ['.xlsx', '.xls']:
        raw_text = extract_text_from_xlsx(file_path)
    elif ext in ['.txt']:
        with open(file_path, 'r', encoding='utf-8') as f:
            raw_text = f.read()
    else:
        raise ValueError(f"Unsupported file extension: {ext}")

    return clean_text(raw_text)

# Example usage
if __name__ == "__main__":
    candidate_file = "data/cvs/sample_candidate.pdf"
    job_desc_file = "data/job_descriptions/sample_job.txt"

    candidate_text = load_and_process_file(candidate_file)
    job_desc_text = load_and_process_file(job_desc_file)

    print("Candidate Text Preview:", candidate_text[:500])
    print("Job Description Preview:", job_desc_text[:500])

