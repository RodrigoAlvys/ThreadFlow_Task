# Procurar Task Através de ID ou Nome
**ID:** RF-10  
**Responsável:** Davi Souza  

---

## Descrição
Funcionalidade de busca que localiza uma task a partir de seu nome ou ID (índice interno) e retorna suas informações.

## Regras De Negócio
- ID é um número inteiro atribuído automaticamente na leitura
- Busca por ID deve ser instantânea (hash map)
- Busca por nome deve ser case-insensitive

## Requisitos Não Funcionais
- Complexidade busca por ID: $O(1)$
- Complexidade busca por nome: $O(n)$ (n = número de tasks)

## Critérios de Aceite
- [ ] **CA1:** Buscar por ID existente retorna a task
- [ ] **CA2:** Buscar por nome existente retorna a task
- [ ] **CA3:** Buscar por termo inexistente retorna "task não encontrada"