import ast
import operator
import re
from collections.abc import Callable
from dataclasses import dataclass


@dataclass(frozen=True)
class ToolCall:
    name: str
    arguments: dict[str, str]


@dataclass(frozen=True)
class ToolResult:
    name: str
    output: str


ToolFunction = Callable[[dict[str, str]], str]


class ToolRegistry:
    def __init__(self) -> None:
        self._tools: dict[str, ToolFunction] = {}

    def register(self, name: str, function: ToolFunction) -> None:
        self._tools[name] = function

    def run(self, call: ToolCall) -> ToolResult:
        if call.name not in self._tools:
            return ToolResult(name=call.name, output=f"Unknown tool: {call.name}")

        output = self._tools[call.name](call.arguments)
        return ToolResult(name=call.name, output=output)

    @property
    def names(self) -> list[str]:
        return sorted(self._tools)


ALLOWED_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
}


def _evaluate_node(node: ast.AST) -> float:
    if isinstance(node, ast.Constant) and isinstance(node.value, int | float):
        return float(node.value)

    if isinstance(node, ast.UnaryOp) and type(node.op) in ALLOWED_OPERATORS:
        return ALLOWED_OPERATORS[type(node.op)](_evaluate_node(node.operand))

    if isinstance(node, ast.BinOp) and type(node.op) in ALLOWED_OPERATORS:
        left = _evaluate_node(node.left)
        right = _evaluate_node(node.right)
        return ALLOWED_OPERATORS[type(node.op)](left, right)

    raise ValueError("Only basic arithmetic expressions are supported")


def calculate(arguments: dict[str, str]) -> str:
    expression = arguments.get("expression", "").strip()
    if not expression:
        return "No expression provided."

    parsed = ast.parse(expression, mode="eval")
    result = _evaluate_node(parsed.body)
    if result.is_integer():
        return str(int(result))
    return str(result)


def summarize(arguments: dict[str, str]) -> str:
    text = arguments.get("text", "").strip()
    if not text:
        return "No text provided."

    sentences = re.split(r"(?<=[.!?])\s+", text)
    first_sentence = sentences[0].strip()
    return first_sentence if first_sentence else text[:240]


def extract_todos(arguments: dict[str, str]) -> str:
    text = arguments.get("text", "").strip()
    if not text:
        return "No todo text provided."

    raw_items = re.split(r",|\n|;|\band\b", text)
    items = [item.strip(" -.") for item in raw_items if item.strip(" -.")]
    return "\n".join(f"- [ ] {item}" for item in items)


def default_registry() -> ToolRegistry:
    registry = ToolRegistry()
    registry.register("calculator", calculate)
    registry.register("summarizer", summarize)
    registry.register("todo_extractor", extract_todos)
    return registry

