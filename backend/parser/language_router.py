import re
from .ast_analyzer import analyze_python_ast

def detect_language(code: str) -> str:
    """Uses regex heuristics to autodetect code language."""
    code_lower = code.lower()
    
    # Go detection (check this before others since it uses packages)
    if re.search(r'\bfunc \w+\(', code) or re.search(r'\bpackage \w+', code) or "fmt.println" in code_lower:
        return "go"

    # Java detection
    if re.search(r'\bpublic class \w+', code) or "system.out.println" in code_lower:
        return "java"

    # JS/TS detection
    if re.search(r'\bfunction \w+\(', code) or re.search(r'\bconst \w+\s*=', code) or "console.log" in code:
        return "javascript"
        
    # Python detection fallback heuristic
    if re.search(r'\bdef \w+\(', code) or re.search(r'\bimport \w+', code) or "print(" in code:
        return "python"
        
    return "python" # absolute fallback


def route_and_parse(code: str, language: str) -> dict:
    """Routes the source code to the appropriate language parser."""
    lang = language.lower()
    
    if lang == "python":
        return analyze_python_ast(code)
    elif lang in ["javascript", "js", "typescript", "ts"]:
        # Fallback heuristic analysis for languages without local AST logic implemented
        return {"note": "AST parsing for JS/TS is deferred to the LLM agent."}
    elif lang in ["java"]:
        return {"note": "AST parsing for Java is deferred to the LLM agent."}
    elif lang in ["go", "golang"]:
        return {"note": "AST parsing for Go is deferred to the LLM agent."}
    else:
        return {"note": f"Unsupported language specific parsing: {lang}. Relying entirely on LLM capability."}
