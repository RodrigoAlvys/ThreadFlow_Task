# Mostrar Informações Básicas da Árvore
**ID:** RF-08  
**Responsável:** Luiz Arthur  

---

## Descrição
Exibe um resumo estatístico da árvore de dependências, incluindo número de tasks, número total de dependências, task com mais dependências (maior out-degree) e task mais requisitada (maior in-degree).

## Regras De Negócio
- Task com mais dependências = aquela que depende de mais outras
- Task mais requisitada = aquela que é dependência de mais outras

## Requisitos Não Funcionais
- Cálculo deve ser $O(n + m)$

## Critérios de Aceite
- [ ] **CA1:** Exibir número total de tasks
- [ ] **CA2:** Exibir número total de dependências
- [ ] **CA3:** Exibir task com mais dependências
- [ ] **CA4:** Exibir task mais requisitada