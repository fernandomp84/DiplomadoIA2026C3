import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage


def call_llm(prompt: str, config: dict) -> str:
    env_file = config["paths"]["env_file"]
    load_dotenv(env_file)

    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise ValueError("No se encontró OPENAI_API_KEY en el archivo .env")

    llm_config = config["llm"]

    llm = ChatOpenAI(
        openai_api_base=llm_config["api_base"],
        openai_api_key=api_key,
        model_name=llm_config["model_name"],
        temperature=float(llm_config["temperature"])
    )

    response = llm.invoke([
        HumanMessage(content=prompt)
    ])

    return response.content.strip()