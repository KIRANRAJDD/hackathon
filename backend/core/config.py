import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Toggle this to False if you configure an actual API key
    USE_MOCK_LLM: bool = os.getenv("USE_MOCK_LLM", "false").lower() == "true"
    
    # Enter your API key here to generate real tests
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    
    # Alternatively, you can use Gemini
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    
    # Alternatively, use Groq
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")

    class Config:
        env_file = ".env"

settings = Settings()
