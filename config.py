"""
Configuration module for DSPy and OpenAI settings
"""
import os
from dotenv import load_dotenv
import dspy

# Load environment variables
load_dotenv()

class Config:
    """Configuration class for the Skilloom AI Agents system"""
    
    # OpenAI Configuration
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    DSPY_MODEL = os.getenv("DSPY_MODEL", "gpt-4o-mini")
    DSPY_MAX_TOKENS = int(os.getenv("DSPY_MAX_TOKENS", "2000"))
    DSPY_TEMPERATURE = float(os.getenv("DSPY_TEMPERATURE", "0.1"))
    
    # Project Configuration
    PROJECT_NAME = os.getenv("PROJECT_NAME", "skilloom_ai_agents")
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    
    # Data Paths
    CVS_PATH = os.getenv("CVS_PATH", "data/cvs")
    JOB_DESCRIPTIONS_PATH = os.getenv("JOB_DESCRIPTIONS_PATH", "data/job_descriptions")
    EVALUATIONS_PATH = os.getenv("EVALUATIONS_PATH", "data/evaluations")
    TRAINING_EXAMPLES_PATH = os.getenv("TRAINING_EXAMPLES_PATH", "data/training_examples")
    
    @classmethod
    def validate_config(cls):
        """Validate that all required configuration is present"""
        if not cls.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is required but not set")
        
        # Create data directories if they don't exist
        for path in [cls.CVS_PATH, cls.JOB_DESCRIPTIONS_PATH, 
                    cls.EVALUATIONS_PATH, cls.TRAINING_EXAMPLES_PATH]:
            os.makedirs(path, exist_ok=True)
    
    @classmethod
    def setup_dspy(cls):
        """Initialize DSPy with OpenAI configuration (compatible with dspy.LM)"""
        cls.validate_config()
        lm = dspy.LM(
            model=cls.DSPY_MODEL,
            api_key=cls.OPENAI_API_KEY
        )
        dspy.configure(lm=lm)
        print(f"DSPy configured with model: {cls.DSPY_MODEL}")
        return lm

# Initialize DSPy on import
if Config.OPENAI_API_KEY:
    Config.setup_dspy()
else:
    print("Warning: OPENAI_API_KEY not found. Please set it in .env file")