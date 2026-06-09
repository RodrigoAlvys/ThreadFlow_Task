#!/usr/bin/env python3
"""
Gerador de arquivo de teste para ThreadFlow_Task
10.000 tasks, 25.000 dependências, com deadloop oculto
"""

import random
import json

NUM_TASKS = 10000
NUM_DEPENDENCIES = 25000
CYCLE_SIZE = 5

print(f"Gerando {NUM_TASKS} tasks...")

tasks = []

# Task raiz
tasks.append({
    "id": 0,
    "name": "ROOT",
    "depends_on": []
})

# Gera tasks em niveis
current_id = 1
level_tasks = [0]

while current_id < NUM_TASKS:
    next_level = []
    for _ in range(min(100, NUM_TASKS - current_id)):
        if not level_tasks:
            deps = []
        else:
            num_deps = random.randint(1, min(3, len(level_tasks)))
            deps = random.sample(level_tasks, num_deps)
        
        tasks.append({
            "id": current_id,
            "name": f"T{current_id}",
            "depends_on": deps
        })
        next_level.append(current_id)
        current_id += 1
    
    level_tasks = next_level

# Adiciona dependencias extras
current_deps = sum(len(t["depends_on"]) for t in tasks)
print(f"Dependencias atuais: {current_deps}")

for _ in range(NUM_DEPENDENCIES - current_deps):
    task_id = random.randint(0, NUM_TASKS - 1)
    dep_id = random.randint(0, NUM_TASKS - 1)
    
    while dep_id == task_id:
        dep_id = random.randint(0, NUM_TASKS - 1)
    
    task = tasks[task_id]
    if dep_id not in task["depends_on"]:
        task["depends_on"].append(dep_id)

# Cria deadloop oculto
cycle_ids = list(range(NUM_TASKS - CYCLE_SIZE, NUM_TASKS))
print(f"Deadloop nas tasks: {cycle_ids}")

for i in range(CYCLE_SIZE):
    task_id = cycle_ids[i]
    next_id = cycle_ids[(i + 1) % CYCLE_SIZE]
    if next_id not in tasks[task_id]["depends_on"]:
        tasks[task_id]["depends_on"].append(next_id)

# Estatisticas finais
total_deps = sum(len(t["depends_on"]) for t in tasks)
print(f"\nTotal de tasks: {len(tasks)}")
print(f"Total de dependencias: {total_deps}")
print(f"Media: {total_deps / len(tasks):.2f}")

# Salva arquivos
with open("teste_10000.txt", "w", encoding="utf-8") as f:
    for t in tasks:
        deps = ",".join(map(str, t["depends_on"])) if t["depends_on"] else ""
        f.write(f"{t['id']};{t['name']};{deps}\n")

with open("teste_10000.json", "w", encoding="utf-8") as f:
    json.dump({"tasks": tasks}, f, indent=2)

print("\nArquivos gerados: teste_10000.txt e teste_10000.json")
