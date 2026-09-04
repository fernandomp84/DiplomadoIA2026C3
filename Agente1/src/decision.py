import importlib
from langchain_core.messages import HumanMessage, SystemMessage

from services.extract_json import extract_json


def build_functions_text(options: dict) -> str:
    lines = []

    for option in options["options"]:
        aliases = ", ".join(option.get("aliases", []))

        lines.append(
            f"- id exacto: {option['id']}\n"
            f"  descripción: {option['description']}\n"
            f"  aliases aceptados: {aliases}"
        )

    return "\n".join(lines)


def load_function(function_path: str):
    module_path, function_name = function_path.rsplit(".", 1)
    module = importlib.import_module(module_path)
    return getattr(module, function_name)


def normalize_text(text: str) -> str:
    return (
        text.lower()
        .strip()
        .replace(" ", "")
        .replace("_", "")
        .replace("-", "")
        .replace("(", "")
        .replace(")", "")
        .replace(",", "")
    )


def find_option_by_id(options: dict, function_id: str) -> dict | None:
    received = normalize_text(function_id)

    for option in options["options"]:
        valid_names = [option["id"]]
        valid_names.extend(option.get("aliases", []))

        for name in valid_names:
            if received == normalize_text(name):
                return option

    return None


def classify_intent(
    llm,
    user_input: str,
    memory,
    classifier_prompt: str,
    options: dict,
    personality: str
) -> dict:

    functions_text = build_functions_text(options)

    system_prompt = classifier_prompt.replace(
        "{functions}",
        functions_text
    )

    system_prompt = f"""
{personality}

{system_prompt}
"""

    history = memory.load_memory_variables({}).get("history", [])

    messages = [
        SystemMessage(content=system_prompt),
        *history,
        HumanMessage(content=user_input)
    ]

    response = llm.invoke(messages)

    return extract_json(response.content)