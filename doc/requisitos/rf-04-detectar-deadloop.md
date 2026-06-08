# Detectar *Deadloop[^1]*
**ID:** RF-04  
**Responsável:** Luiz Arthur 

---

## Descrição
Funcionalidade que detecta dependências circulares (*deadloop[^1]*) entre as tarefas, interrompendo o processamento e retornando uma mensagem de erro clara ao usuário.

## Regras De Negócio
- A detecção deve ocorrer antes da ordenação topológica
- Em caso de *deadloop[^1]*, o programa não deve tentar ordenar as tarefas
- A mensagem de erro deve indicar quais tarefas formam o ciclo

## Requisitos Não Funcionais
- Tolerância a erros
- Complexidade máxima O(n + m), onde n = número de tasks e m = número de dependências

## Critérios de Aceite
- [ ] **CA1:** Detectar ciclo simples (ex.: A → B → A)
- [ ] **CA2:** Detectar ciclo longo (ex.: A → B → C → A)
- [ ] **CA3:** Retornar mensagem clara com as tasks envolvidas no ciclo

---

>[!NOTE]
> Recomendado usar *DFS* com cores como design de referência.

[^1]: Biblioteca de estrutura de dados pensando em grafos e visualização,[**link**](https://networkx.org/documentation/stable/index.html#) oficial do site.