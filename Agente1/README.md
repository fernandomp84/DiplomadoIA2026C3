# Agente1

Agente local básico con:

- configuración en JSON
- metaprompt editable
- decisiones externas
- funciones de decisión modulares
- memoria temporal en RAM
- conexión a LLM vía OpenRouter

## Ejecutar

Desde:

/Users/orodriguez/PycharmProjects/DiplomadoIA/Agente1

Ejecutar:

python src/main.py

## Qué puede modificar el usuario

### Personalidad

Editar:

prompts/personality.txt

### Funciones de decisión

Editar cualquiera de estos archivos:

services/decision_functions/option_a.py
services/decision_functions/option_b.py
services/decision_functions/option_c.py
services/decision_functions/option_d.py

También puede agregar más funciones y registrarlas en:

decisions/options.json