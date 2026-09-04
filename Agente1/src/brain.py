from langchain_core.messages import HumanMessage, SystemMessage

from src.decision import classify_intent, find_option_by_id, load_function


def run_agent_loop(llm, memory, config, classifier_prompt, options, personality):
    max_iterations = int(config["agent"]["max_iterations"])

    print(
        f"💬 Mini-agente listo. Máximo {max_iterations} intentos para identificar la función."
    )
    print("Escribe 'salir' para terminar.\n")

    while True:
        classify_steps = 0
        chosen_option = None

        while chosen_option is None:
            user_input = input("👤 Tú: ").strip()

            if user_input.lower() in {"salir", "exit", "quit"}:
                print("👋 Hasta luego.")
                return

            if not user_input:
                continue

            memory.chat_memory.add_message(
                HumanMessage(content=user_input)
            )

            if classify_steps >= max_iterations:
                print(
                    f"🤖 Bot: No pude identificar la intención en {max_iterations} mensajes. Reformula tu solicitud.\n"
                )
                break

            data = classify_intent(
                llm=llm,
                user_input=user_input,
                memory=memory,
                classifier_prompt=classifier_prompt,
                options=options,
                personality=personality
            )

            classify_steps += 1

            action = data.get("action")

            if action == "ask":
                question = data.get("question", "").strip()

                if not question:
                    question = "¿Puedes aclarar qué operación quieres realizar?"

                print(f"🤖 Bot: {question}\n")

                memory.chat_memory.add_message(
                    SystemMessage(content=f"(bot_ask) {question}")
                )

                continue

            if action == "choose":
                function_id = data.get("function", "").strip()
                chosen_option = find_option_by_id(options, function_id)

                if chosen_option is None:
                    print("🤖 Bot: Esa función no existe. Aclara tu solicitud.\n")
                    continue

                print(chosen_option["id"])

                memory.chat_memory.add_message(
                    SystemMessage(content=f"(bot_choose) {chosen_option['id']}")
                )

                break

            print("🤖 Bot: No entendí la acción. Reformula tu solicitud.\n")

        if chosen_option is None:
            continue

        function = load_function(chosen_option["function"])

        try:
            result = function()
            print(f"✅ Resultado: {result}\n")
        except Exception as error:
            print(f"❌ Error ejecutando la función: {error}\n")