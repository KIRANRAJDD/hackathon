from .ast_analyzer import analyze_python_ast

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
    else:
        return {"note": f"Unsupported language specific parsing: {lang}. Relying entirely on LLM capability."}
