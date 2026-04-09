from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from core.llm_engine import generate_tests_from_llm
from parser.language_router import route_and_parse
from generator.prompt_builder import build_prompt
from generator.output_formatter import check_json_output, save_test_file

app = FastAPI(title="AI Test Generator API")

# Allow requests from our vanilla frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CodeRequest(BaseModel):
    code: str
    language: str

@app.post("/generate")
async def generate_tests(request: CodeRequest):
    if not request.code.strip():
        raise HTTPException(status_code=400, detail="Source code cannot be empty.")
        
    # Phase 1: Parse AST
    ast_analysis = route_and_parse(request.code, request.language)
    
    # Phase 2: Build Prompt
    prompt = build_prompt(request.code, request.language, ast_analysis)
    
    # Phase 3: Call LLM
    try:
        raw_llm_response = await generate_tests_from_llm(prompt)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LLM Generation Failed: {str(e)}")
        
    # Phase 4: Format and Verify
    formatted_output = check_json_output(raw_llm_response)
    
    # Phase 5: Save files to disk
    ext = "py" if request.language.lower() == "python" else "js" if request.language.lower() in ["javascript", "js"] else "txt"
    save_test_file(formatted_output["unit_tests"], f"test_unit.{ext}")
    save_test_file(formatted_output["integration_tests"], f"test_integration.{ext}")
    save_test_file(formatted_output["edge_cases"], f"test_edge.{ext}")

    return {
        "status": "success",
        "ast_analysis": ast_analysis,
        "results": formatted_output,
        "message": "Tests generated and saved successfully!"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
