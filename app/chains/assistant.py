# app/chains/assistant.py
from typing import List, Dict, Any
from openai import OpenAI
from app.config import settings
from app.tools import calculator, search_knowledge
from app.telemetry.mlflow_utils import traced_run, log_chat
from app.rag.retriever import stuff_context

client = OpenAI()

# Carga prompt del sistema
_SYSTEM = open("app/prompts/system_breast_cancer_es.txt", "r", encoding="utf-8").read()

TOOLS = {
    calculator.tool_spec()["name"]: (calculator.tool_spec(), calculator.run),
    search_knowledge.tool_spec()["name"]: (search_knowledge.tool_spec(), search_knowledge.run),
}

def tool_specs() -> List[Dict[str, Any]]:
    return [spec for spec, _ in TOOLS.values()]

SAFETY_TOPICS = {"diagnóstico", "dosis", "tratamiento definitivo", "receta"}

def safety_guardrail(user_text: str) -> Dict[str, Any]:
    flags = {"clinical_risk": any(w in user_text.lower() for w in SAFETY_TOPICS)}
    return flags

def run_tool(name: str, args: Dict[str, Any]) -> str:
    spec, fn = TOOLS[name]
    return fn(**args) if name != "local_search" else str(fn(args.get("query")))

def chat(user_text: str) -> Dict[str, Any]:
    flags = safety_guardrail(user_text)

    rag_context = stuff_context(user_text)
    messages=[
        {"role": "system", "content": _SYSTEM + "\n\nUsa el contexto si es relevante, cítalo como 'contexto interno'."},
        {"role": "user", "content": user_text + "\n\n" + rag_context},
    ]

    with traced_run("chat", params={"model": settings.OPENAI_MODEL, "env": settings.ENV, **flags}):
        response = client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            temperature=settings.TEMPERATURE,
            max_tokens=settings.MAX_TOKENS,
            tools=[{"type": "function", "function": t} for t in tool_specs()],
            messages=messages,
        )

        msg = response.choices[0].message
        input_tokens = response.usage.prompt_tokens if hasattr(response, "usage") else None
        output_tokens = response.usage.completion_tokens if hasattr(response, "usage") else None

        # Si el modelo pide herramienta
        if getattr(msg, "tool_calls", None):
            tool_call = msg.tool_calls[0]
            name = tool_call.function.name
            args = tool_call.function.arguments
            tool_result = run_tool(name, args)
            log_chat(input_tokens, output_tokens, tool_used=name, safety_flags=flags)

            # Segunda llamada con resultado de la herramienta
            followup = client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                temperature=settings.TEMPERATURE,
                max_tokens=settings.MAX_TOKENS,
                messages=[
                    {"role": "system", "content": _SYSTEM},
                    {"role": "user", "content": user_text + "\n\n" + rag_context},
                    msg,
                    {"role": "tool", "tool_call_id": tool_call.id, "name": name, "content": str(tool_result)},
                ],
            )
            final = followup.choices[0].message
            output_tokens2 = followup.usage.completion_tokens if hasattr(followup, "usage") else None
            log_chat(None, output_tokens2, tool_used=name, safety_flags=None)
            return {"content": final.content, "tool_used": name}

        log_chat(input_tokens, output_tokens, tool_used=None, safety_flags=flags)
        return {"content": msg.content, "tool_used": None}
