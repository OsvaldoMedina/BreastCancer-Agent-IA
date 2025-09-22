# app/tools/calculator.py
from typing import Dict, Any

def tool_spec() -> Dict[str, Any]:
    return {
        "name": "calculator",
        "description": "Operaciones aritméticas simples y seguras.",
        "schema": {
            "type": "object",
            "properties": {
                "expression": {"type": "string", "description": "Expresión, e.g., '2+2*3'"}
            },
            "required": ["expression"],
        },
    }

ALLOWED = set("0123456789.+-*/() ")

def run(expression: str) -> str:
    if not set(expression) <= ALLOWED:
        return "Expresión no permitida"
    try:
        return str(eval(expression, {"__builtins__": {}}, {}))
    except Exception as e:
        return f"Error: {e}"
