# Demonstração Visual da Árvore em ASCII
**ID:** RF-07  
**Responsável:** Davi Souza  

---

## Descrição
Funcionalidade que exibe a árvore de dependências no terminal usando caracteres ASCII, representando a hierarquia entre tarefas.

## Regras De Negócio
- A raiz são tarefas sem dependências
- Tarefas dependentes são mostradas como filhos

## Requisitos Não Funcionais
- Funciona em qualquer terminal que suporte ASCII básico

## Critérios de Aceite
- [ ] **CA1:** Exibir árvore corretamente para até 20 tarefas
- [ ] **CA2:** Não quebrar layout para tarefas com nomes longos (truncar se necessário)