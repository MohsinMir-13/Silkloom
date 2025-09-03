# Skilloom

Skilloom is an AI-powered platform for automated CV evaluation, job matching, and professional communication.

## Features
- Batch and single CV processing
- Job description parsing
- Email and report generation for candidates
- Interactive CLI and web interface (Streamlit)
- Save and download results
- Git integration for version control

## Project Structure
- `agents/`: Modular AI agents for CV analysis, job info collection, email/report generation
- `data/`: Example CVs, job descriptions, evaluations, training examples
- `output/`: Generated emails and reports
- `optimization/`: Agent compilation and metric functions
- `preprocessing/`: Data pipeline for file loading and processing
- `signatures/`: Signature definitions for agent tasks
- `app.py`: Streamlit web interface
- `cli.py`: Interactive and batch CLI interface
- `main.py`: Example batch pipeline
- `config.py`: Configuration and DSPy setup

## Setup
1. Clone the repository:
   ```sh
   git clone https://github.com/MohsinMir-13/Silkloom.git
   cd Silkloom
   ```
2. Create and activate a Python virtual environment:
   ```sh
   python3 -m venv skilloom-env
   source skilloom-env/bin/activate
   ```
3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
4. Set your OpenAI API key in a `.env` file:
   ```sh
   echo "OPENAI_API_KEY=your-key-here" > .env
   ```

## Usage
### CLI
Run the interactive CLI:
```sh
python cli.py
```
Or batch process:
```sh
python cli.py --job data/job_descriptions/sample_job.txt --cvs data/cvs/*.pdf data/cvs/*.txt --output output/
```

### Web Interface
Start the Streamlit app:
```sh
streamlit run app.py
```

## Data Format
- CVs: PDF or TXT files, or pasted text
- Job Descriptions: TXT files, or pasted text
- Outputs: Emails and reports saved in `output/`

## Contributing
Pull requests and issues are welcome!
