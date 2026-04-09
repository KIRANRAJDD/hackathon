import os

def check_json_output(response: dict) -> dict:
    """Verifies and formats the LLM output."""
    # In a real implementation this might parse markdown codeblocks into raw json
    # Because we enforced JSON in the prompt, we expect a dict back from llm_engine if we decode it.
    
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
