import os

def check_json_output(response: dict) -> dict:
    """Verifies and formats the LLM output."""
    # Ensure it's a dict to prevent crashes if parsing failed
    if not isinstance(response, dict):
        return {
            "summary": "Error: LLM Engine failed to produce a valid JSON dictionary.",
            "scenarios": [],
            "unit_tests": "No unit tests generated.",
            "integration_tests": "No integration tests generated.",
            "edge_cases": "No edge cases generated."
        }
        
    expected_keys = ["summary", "scenarios", "unit_tests", "integration_tests", "edge_cases"]
    for key in expected_keys:
        if key not in response:
            response[key] = f"No {key} generated."
            
    return response

def save_test_file(code: str, filename: str) -> str:
    """Saves the generated tests into the output directory."""
    out_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'output_tests'))
    os.makedirs(out_dir, exist_ok=True)
    
    filepath = os.path.join(out_dir, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(code)
        
    return filepath
