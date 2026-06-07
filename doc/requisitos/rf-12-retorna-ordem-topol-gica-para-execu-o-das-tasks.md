# Retorna Ordem Topológica para Execução das Tasks
**ID:** RF-12  
**Responsável:** Rodrigo Alves  

---

## Descrição
Ordena as tarefas topologicamente (da que não depende de nenhuma para a que depende de todas as anteriores), garantindo que, ao executar na ordem retornada, todas as dependências de uma task já foram satisfeitas.

## Regras De Negócio
- Usar algoritmo de Kahn ou DFS com pilha
- Proibido uso de bibliotecas prontas como *networkx[^1]*
- Se houver *deadloop[^2]*, a ordem não é gerada e um erro é retornado

## Requisitos Não Funcionais
- Complexidade $O(n + m)$
- Tratamento correto de tarefas sem dependências (devem vir primeiro)

## Critérios de Aceite
- [ ] **CA1:** Para entradas sem ciclo, retorna lista ordenada
- [ ] **CA2:** Se A depende de B, B aparece antes de A na ordem
- [ ] **CA3:** Em caso de ciclo, retorna erro (não ordena)

---

[^1]: Biblioteca de estrutura de dados pensando em grafos e visualização,[**link**](https://networkx.org/documentation/stable/index.html#) oficial do site.
[^2]: *Deadloop* são dependências cíclicas que ocorrem quando dois ou mais processos ficam bloqueados indefinidamente por dependerem mutuamente dos recursos que o outro possui, gerando um impasse.