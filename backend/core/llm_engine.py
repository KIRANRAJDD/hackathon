import json
import logging
from .config import settings

logger = logging.getLogger(__name__)

async def generate_tests_from_llm(prompt: str) -> dict:
    """
    Sends the fully constructed prompt to the LLM (or mock) and returns structured JSON.
    """
    if settings.USE_MOCK_LLM:
        logger.info("Using MOCK LLM response. (Set USE_MOCK_LLM=False and provide an API key in config to generate real tests).")
        return _get_mock_response()
    
    elif settings.OPENAI_API_KEY:
        logger.info("Using OpenAI integration.")
        # This is where you would call openai.AsyncOpenAI().chat.completions.create(...)
        # For simplicity in this mock structure, we simulate a failure if the package isn't installed.
        raise NotImplementedError("OpenAI client not fully implemented. Please use MOCK_LLM or implement the OpenAI API call here.")
        
    elif settings.GEMINI_API_KEY:
        logger.info("Using Gemini integration.")
        # This is where you would call google.generativeai.generate_content(...)
        raise NotImplementedError("Gemini client not fully implemented. Please use MOCK_LLM or implement the Gemini API call here.")
        
    else:
        raise ValueError("No LLM provider configured and USE_MOCK_LLM is false.")

def _get_mock_response() -> dict:
    """Returns a highly detailed mock response for demonstration."""
    return {
        "summary": "The provided codebase is a Python script that calculates factorial. The core logic involves a recursive or iterative function. The component is standalone with no external dependencies. A recursion depth edge case is detected.",
        "scenarios": [
            "Unit test for standard positive integers (e.g., 5).",
            "Edge case test for 0 (should return 1).",
            "Exception edge case for negative integers.",
            "Type error edge case for passing a string or float."
        ],
        "unit_tests": "import pytest\nfrom main import calculate_factorial\n\nclass TestFactorial:\n    def test_factorial_positive(self):\n        assert calculate_factorial(5) == 120\n\n    def test_factorial_zero(self):\n        assert calculate_factorial(0) == 1",
        "integration_tests": "# No distinct integration patterns required for an isolated math function.\n# If it was part of a math suite, we would test it inside other components here.\npass",
        "edge_cases": "    def test_factorial_negative(self):\n        with pytest.raises(ValueError):\n            calculate_factorial(-1)\n\n    def test_factorial_type(self):\n        with pytest.raises(TypeError):\n            calculate_factorial('abc')"
    }
