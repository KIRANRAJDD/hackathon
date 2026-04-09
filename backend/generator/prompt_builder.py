def build_prompt(code: str, language: str, ast_analysis: dict) -> str:
    """Builds the comprehensive system prompt for the LLM."""
    
    ast_context = ""
    if ast_analysis and "error" not in ast_analysis:
        ast_context = f"\n\nPre-parsed Code Context:\nImports: {ast_analysis.get('imports', [])}\nFunctions: {ast_analysis.get('functions', [])}\nClasses: {ast_analysis.get('classes', [])}"

    prompt = f"""You are an expert AI software testing engineer. Your task is to analyze the given codebase and automatically generate high-quality test cases for {language}.

### Objectives:
1. Analyze the provided source code including Functions, Classes, Methods, Modules, and Dependencies.
2. Generate:
   - Unit Tests
   - Integration Tests
   - Edge Case Tests (boundary values, invalid inputs, exceptions)
3. Ensure high code coverage and meaningful assertions.
4. Use standard testing frameworks (pytest for python, Jest for JS, JUnit for Java).

### Input Code:
```{language}
{code}
```
{ast_context}

### Output Instructions:
You MUST respond IN STRICT JSON FORMAT with the following keys exactly:
- "summary": (string) Brief analysis summary.
- "scenarios": (list of strings) Identified test scenarios.
- "unit_tests": (string) The runnable unit test code block.
- "integration_tests": (string) The runnable integration test code block.
- "edge_cases": (string) The runnable edge cases code block.
"""
    return prompt
