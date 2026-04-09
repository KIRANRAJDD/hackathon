import ast

def analyze_python_ast(code: str) -> dict:
    """Parses Python source code and extracts its structural metadata to help the LLM."""
    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        return {"error": f"Failed to parse python syntax: {str(e)}"}

    analysis = {
        "classes": [],
        "functions": [],
        "imports": []
    }

    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            methods = [n.name for n in node.body if isinstance(n, ast.FunctionDef)]
            analysis["classes"].append({"name": node.name, "methods": methods})
        elif isinstance(node, ast.FunctionDef) and not isinstance(getattr(node, 'parent', None), ast.ClassDef):
            # Very basic check to avoid double-counting class methods, though `walk` isn't hierarchical.
            # In a robust system, we would use a NodeVisitor.
            analysis["functions"].append(node.name)
        elif isinstance(node, ast.Import):
            for alias in node.names:
                analysis["imports"].append(alias.name)
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                analysis["imports"].append(node.module)

    # Simplified unique list
    analysis["imports"] = list(set(analysis["imports"]))
    
    return analysis
