# Construir Árvore De Requisitos
**ID:** RF-03  
**Responsável:** Rodrigo Alves  

---

## Descrição Geral
A árvore de requisitos tem como funcionalidade organizar as tasks e dependências em nós e arestas, onde o filho é dependente do pai, dessa forma, facilitando o encontro de uma ordem topológica, rodar todas as tasks, e *deadloop[^2]*.
## Regras De Negócio
- Proibido uso de bibliotecas de alto nível, exemplo: *networkx[^1]*
- Criação de estrutura de dados próprios
- O nodo filho deve ser dependente do pai 

## Requisitos Não Funcionais
- Tolerância a erro
- Complexidade da árvore deve ser de Big $O(n \log n)$

## Critério De Aceite
- [ ] **CA1:** Nós da árvore deve ser organizada de modo que nó A depende de nó B
- [ ] **CA2:** Complexidade da árvore deverá ser Big $O(n \log n)$

[^1]: Biblioteca de estrutura de dados pensando em grafos e visualização,[**link**](https://networkx.org/documentation/stable/index.html#) oficial do site.
[^2]: *Deadloop* são dependências cíclicas que ocorrem quando dois ou mais processos ficam bloqueados indefinidamente por dependerem mutuamente dos recursos que o outro possui, gerando um impasse.