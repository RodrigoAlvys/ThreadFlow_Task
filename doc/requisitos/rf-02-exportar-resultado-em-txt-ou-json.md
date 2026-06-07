# Exportar Resultado em `.txt` ou `.json`
**ID:** RF-02  
**Responsável:** Davi Souza  

---

## Descrição
Funcionalidade que exporta a lista de tarefas ordenada topologicamente (ou a árvore processada) para um arquivo no formato `.txt` ou `.json`, conforme especificado pelo usuário.

## Regras De Negócio
- O formato de saída deve ser o mesmo do informado no parâmetro `--of`
- No `.txt`, cada task deve ser listada em ordem, uma por linha
- No `.json`, deve ser exportado um dicionário com chave `"ordem_topologica"` e valor a lista de tasks

## Requisitos Não Funcionais
- Resistência a erros (ex.: permissão de escrita negada)

## Critérios de Aceite
- [ ] **CA1:** Exportar lista ordenada para `.txt` com uma task por linha
- [ ] **CA2:** Exportar lista ordenada para `.json` com estrutura `{"ordem_topologica": ["task1", "task2"]}`