# Mostrar Informações Básicas Específica de uma Task
**ID:** RF-09  
**Responsável:** Davi Souza  

---

## Descrição
Exibe informações detalhadas de uma task específica: suas dependências (tasks que ela precisa) e seus dependentes (tasks que dependem dela).

## Regras De Negócio
- A task pode ser informada por nome ou ID
- Se a task não existir, retornar erro

## Requisitos Não Funcionais
- Busca por ID com complexidade $O(1)$
- Busca por nome com complexidade $O(\log n)$ ou $O(n)$, mas documentada

## Critérios de Aceite
- [ ] **CA1:** Exibir "depende de: [lista]" para a task
- [ ] **CA2:** Exibir "é requisitada por: [lista]" para a task
- [ ] **CA3:** Retornar erro claro se task não existir