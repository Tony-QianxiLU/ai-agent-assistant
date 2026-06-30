from dataclasses import dataclass


@dataclass(frozen=True)
class MemoryEntry:
    step: str
    content: str


def render_memory(memory: list[MemoryEntry]) -> str:
    if not memory:
        return "No execution memory recorded."

    return "\n".join(f"{entry.step}: {entry.content}" for entry in memory)
