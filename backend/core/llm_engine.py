import json
import logging
from .config import settings

try:
    from google import genai
    from google.genai import types
except ImportError:
    pass

logger = logging.getLogger(__name__)

async def generate_tests_from_llm(prompt: str) -> dict:
    """
    Sends the fully constructed prompt to the LLM (or mock) and returns structured JSON.
    """
    if settings.USE_MOCK_LLM:
        logger.info("Using MOCK LLM response. (Set USE_MOCK_LLM=False and provide an API key in config to generate real tests).")
        return _get_mock_response()
    
    elif settings.GEMINI_API_KEY:
        logger.info("Using Gemini integration.")
        client = genai.Client(api_key=settings.GEMINI_API_KEY)
        
        try:
            # We configure it directly to return pure JSON
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                ),
            )
            raw_text = response.text
            
            # Since we enforced JSON via the prompt and mime_type, we can safely parse
            try:
                parsed_data = json.loads(raw_text)
                return parsed_data
            except json.JSONDecodeError as decode_err:
                logger.error(f"Failed to decode JSON from Gemini: {raw_text}")
                # Fallback to mock on parsing error so the UI doesn't crash completely during dev
                return _get_mock_response()

        except Exception as e:
            logger.error(f"Gemini API failed: {str(e)}")
            raise e
            
    elif settings.OPENAI_API_KEY:
        logger.info("Using OpenAI integration.")
        raise NotImplementedError("OpenAI client not fully implemented. Please use MOCK_LLM or implement the OpenAI API call here.")
        
    else:
        raise ValueError("No LLM provider configured and USE_MOCK_LLM is false.")

def _get_mock_response() -> dict:
    """Returns a highly detailed mock response for demonstration/fallback."""
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
