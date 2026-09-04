def create_memory() -> list:
    return []


def add_to_memory(memory: list, role: str, content: str) -> None:
    memory.append({
        "role": role,
        "content": content
    })


def get_recent_memory(memory: list, limit: int = 10) -> list:
    return memory[-limit:]