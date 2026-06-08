import json


def read_txt(file_path):
    tasks = []

    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()

            if not line:
                continue

            parts = line.split(";")

            task_id = int(parts[0])
            task_name = parts[1]

            dependencies = []

            if len(parts) > 2 and parts[2]:
                dependencies = [int(dep) for dep in parts[2].split(",")]

            tasks.append({
                "id": task_id,
                "name": task_name,
                "depends_on": dependencies
            })

    return tasks


def read_json(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    return data["tasks"]


def load_file(file_path):
    if file_path.endswith(".txt"):
        return read_txt(file_path)

    if file_path.endswith(".json"):
        return read_json(file_path)

    raise ValueError("Formato inválido. Utilize .txt ou .json")