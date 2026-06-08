import json

from .tree_json import requirements_tree_to_json


DEFAULT_MAX_NAME_LENGTH = 40


def _truncate(text, max_length):
    text = str(text)

    if len(text) <= max_length:
        return text

    if max_length <= 3:
        return text[:max_length]

    return text[: max_length - 3] + "..."


def _task_label(task, max_name_length):
    name = _truncate(task.get("name", ""), max_name_length)

    return f"[{task['id']}] {name}"


def _format_node(task, prefix, is_last, max_name_length, lines):
    connector = "`-- " if is_last else "|-- "
    lines.append(prefix + connector + _task_label(task, max_name_length))

    children = task.get("children", [])
    next_prefix = prefix + ("    " if is_last else "|   ")

    for index, child in enumerate(children):
        _format_node(
            child,
            next_prefix,
            index == len(children) - 1,
            max_name_length,
            lines,
        )


def requirements_tree_to_ascii(tasks, max_name_length=DEFAULT_MAX_NAME_LENGTH):
    data = json.loads(requirements_tree_to_json(tasks))

    if data["erro"]:
        return f"erro: {data['erro']}"

    lines = []
    roots = data["arvore"]

    for index, root in enumerate(roots):
        _format_node(
            root,
            "",
            index == len(roots) - 1,
            max_name_length,
            lines,
        )

    return "\n".join(lines)


def print_requirements_tree(tasks, max_name_length=DEFAULT_MAX_NAME_LENGTH):
    ascii_tree = requirements_tree_to_ascii(tasks, max_name_length)
    print(ascii_tree)
    return ascii_tree
