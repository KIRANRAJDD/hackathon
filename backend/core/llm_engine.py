import json
import logging
from .config import settings

try:
    from google import genai
    from google.genai import types
except ImportError:
    pass

try:
    from groq import Groq
except ImportError:
    pass

logger = logging.getLogger(__name__)

async def generate_tests_from_llm(prompt: str, code: str = "") -> dict:
    """
    Sends the fully constructed prompt to the LLM (or mock) and returns structured JSON.
    """
    if settings.USE_MOCK_LLM:
        logger.info("Using MOCK LLM response. (Set USE_MOCK_LLM=False and provide an API key in config to generate real tests).")
        return _get_mock_response(code)
    
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
                return _get_mock_response(code)

        except Exception as e:
            logger.error(f"Gemini API failed: {str(e)}")
            raise e
            
    elif settings.GROQ_API_KEY:
        logger.info("Using Groq integration.")
        client = Groq(api_key=settings.GROQ_API_KEY)
        
        try:
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": "You must respond with valid JSON containing the keys: 'summary', 'scenarios', 'unit_tests', 'integration_tests', and 'edge_cases'."},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.2
            )
            raw_text = response.choices[0].message.content
            
            try:
                parsed_data = json.loads(raw_text)
                return parsed_data
            except json.JSONDecodeError as decode_err:
                logger.error(f"Failed to decode JSON from Groq: {raw_text}")
                return _get_mock_response(code)

        except Exception as e:
            logger.error(f"Groq API failed: {str(e)}")
            raise e
            
    elif settings.OPENAI_API_KEY:
        logger.info("Using OpenAI integration.")
        raise NotImplementedError("OpenAI client not fully implemented. Please use MOCK_LLM or implement the OpenAI API call here.")
        
    else:
        raise ValueError("No LLM provider configured and USE_MOCK_LLM is false.")

def _get_mock_response(code: str = "") -> dict:
    """Returns a dynamic mock response based on the input code for demonstration/fallback."""
    # Try to extract the first function or class name from the code
    target_name = "example_function"
    if code:
        for line in code.splitlines():
            line = line.strip()
            if line.startswith("def "):
                target_name = line.split("def ")[1].split("(")[0].strip()
                break
            elif line.startswith("class "):
                target_name = line.split("class ")[1].split("(")[0].split(":")[0].strip()
                break

    return {
        "summary": f"The provided codebase contains the '{target_name}' component. The core logic has been analyzed and standard test scenarios have been identified.",
        "scenarios": [
            f"Unit test for expected behavior of {target_name}.",
            f"Edge case test for bounding limits in {target_name}.",
            f"Exception edge case for invalid inputs provided to {target_name}."
        ],
        "unit_tests": f"import pytest\nfrom main import {target_name}\n\nclass Test{target_name.capitalize()}:\n    def test_{target_name}_positive(self):\n        # Mock assertion\n        assert True\n\n    def test_{target_name}_negative(self):\n        # Mock assertion\n        assert True",
        "integration_tests": "# No distinct integration patterns required for an isolated function.\n# If it was part of a larger suite, we would mock boundaries here.\npass",
        "edge_cases": f"    def test_{target_name}_edge(self):\n        with pytest.raises(Exception):\n            # Mock forcing exception\n            raise ValueError('Invalid Input')"
    }
