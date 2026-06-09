# ThreadFlow_Task

## Integrantes

- Rodrigo Alves Barboza da Silva
- Davi Souza Mendonça
- Luiz Arthur da Silva Costa

---

# 1. Visão Geral

O **ThreadFlow_Task** é uma aplicação de linha de comando (CLI) desenvolvida em Python para organizar tarefas dependentes através de uma estrutura de grafo direcionado.

O sistema recebe uma lista de tarefas em formato `.txt` ou `.json`, constrói uma árvore de dependências, detecta dependências circulares (deadloops), gera a ordem topológica de execução e exporta os resultados em diferentes formatos.

O projeto foi desenvolvido sem o uso de bibliotecas especializadas em grafos, implementando todas as estruturas de dados e algoritmos necessários de forma própria.

---

# 2. Objetivo

Permitir que programadores, agentes autônomos e equipes de desenvolvimento organizem tarefas dependentes de maneira segura, identificando ciclos e produzindo uma sequência válida de execução.

---

# 3. Tecnologias Utilizadas

- Python 3.9+
- JSON
- Biblioteca padrão do Python

Bibliotecas utilizadas:

- json
- collections
- os
- sys

Não foram utilizadas bibliotecas de grafos de alto nível como NetworkX.

---

# 4. Estrutura do Projeto

```text
ThreadFlow_Task/
│
├── src/
│   ├── cli/
│   │   └── menu.py
│   │
│   ├── graph/
│   │   ├── __init__.py
│   │   ├── requirement_graph.py
│   │   ├── task_node.py
│   │   └── tree_builder.py
│   │
│   ├── cycle_detector.py
│   ├── file_reader.py
│   ├── main.py
│   ├── task_info.py
│   ├── task_search.py
│   ├── tree_ascii.py
│   ├── tree_json.py
│   └── tree_stats.py
│
├── data/
│   ├── generate.py
│   ├── teste_10000.txt
│   └── teste_10000.json
│
├── LICENSE
├── run.bat
├── run.sh
└── README.md
```

---

# 5. Execução

## Windows

```bash
run.bat
```

### Executar arquivo

```bash
run.bat --if=entrada.txt
```

### Exportar resultado

```bash
run.bat --if=entrada.txt --of=saida.json
```

---

## Linux / Unix

```bash
./run.sh
```

### Executar arquivo

```bash
./run.sh --if=entrada.txt
```

### Exportar resultado

```bash
./run.sh --if=entrada.txt --of=saida.json
```

---

## Execução direta com Python

Modo interativo:

```bash
python src/main.py
```

Modo arquivo:

```bash
python src/main.py --if=entrada.txt
```

Modo exportação:

```bash
python src/main.py --if=entrada.txt --of=saida.json
```

---

# 6. Arquitetura da Solução

Fluxo principal do sistema:

```text
Arquivo TXT/JSON
        │
        ▼
   File Reader
        │
        ▼
 Requirement Graph
        │
        ▼
 Cycle Detector
        │
        ▼
  Tree Builder
        │
        ├── Ordem Topológica
        ├── Estatísticas
        ├── Busca
        ├── Árvore ASCII
        └── Exportação
```

## Justificativa da Arquitetura

O sistema foi dividido em módulos independentes para reduzir o acoplamento e aumentar a manutenibilidade do código.

Cada módulo possui uma responsabilidade específica:

- **file_reader**: leitura e interpretação dos arquivos de entrada.
- **RequirementGraph**: armazenamento das relações de dependência.
- **cycle_detector**: validação de dependências circulares.
- **TreeBuilder**: construção da árvore hierárquica.
- **task_search**: mecanismo de busca otimizado.
- **tree_ascii** e **tree_json**: visualização e exportação dos dados.

Essa separação facilita testes, manutenção e futuras expansões do projeto. Como cada componente possui uma função bem definida, alterações em uma parte do sistema tendem a causar pouco impacto nas demais partes da aplicação.

---

# 7. Estruturas de Dados Utilizadas

## 7.1 Grafo Direcionado

Estrutura principal do sistema.

Cada tarefa é representada como um vértice e cada dependência é representada como uma aresta direcionada.

Exemplo:

```text
Backend → Frontend → Deploy
```

### Justificativa

O problema tratado pelo sistema consiste em relações de dependência entre tarefas.

Como uma tarefa pode depender de várias outras e também ser pré-requisito para diversas tarefas simultaneamente, uma estrutura linear não seria adequada.

O grafo direcionado permite representar naturalmente essas relações através de:

- Vértices → tarefas.
- Arestas direcionadas → dependências.

Além disso, algoritmos clássicos como DFS e ordenação topológica trabalham diretamente sobre grafos, reduzindo a complexidade da solução.

---

## 7.2 Árvore de Dependências

Após a validação do grafo, uma árvore hierárquica é construída para visualização e navegação.

### Justificativa

Embora o grafo seja a estrutura principal para processamento, sua visualização pode ser difícil para usuários finais.

Por esse motivo foi construída uma representação em árvore, que organiza as tarefas de forma hierárquica e facilita a compreensão das dependências.

Essa estrutura é utilizada principalmente para:

- Exibição ASCII.
- Navegação visual.
- Exportação estruturada.

---

## 7.3 Tabelas Hash (Dicionários)

Utilizadas para indexação por:

- ID
- Nome

Exemplo:

```python
nodes_by_id
nodes_by_name
_tasks_by_id
_tasks_by_name
```

### Complexidade

```text
O(1)
```

### Justificativa

As operações de busca são uma das funcionalidades mais utilizadas do sistema.

Uma implementação baseada apenas em listas exigiria percorrer todos os elementos até encontrar a tarefa desejada.

Utilizando tabelas hash, o acesso ocorre diretamente pela chave:

- ID da tarefa.
- Nome da tarefa.

Essa escolha reduz a complexidade de busca de O(n) para O(1), atendendo explicitamente aos requisitos não funcionais do projeto.

---

## 7.4 Filas (Deque)

Utilizadas pelo algoritmo de Kahn para ordenação topológica.

### Complexidade

```text
O(1)
```

por inserção e remoção.

### Justificativa

O algoritmo de Kahn necessita processar continuamente tarefas sem dependências pendentes.

A estrutura de fila permite:

- Inserções rápidas.
- Remoções rápidas.
- Processamento em ordem adequada.

A implementação com deque foi escolhida por oferecer operações eficientes nas extremidades da estrutura.

---

## 7.5 Conjuntos (Set)

Utilizados para:

- Controle de visitados.
- Detecção de ciclos.
- Evitar processamento repetido.

### Complexidade

```text
O(1)
```

para operações de consulta.

### Justificativa

Durante a detecção de ciclos e construção da árvore é necessário verificar repetidamente se um nó já foi visitado.

A utilização de conjuntos reduz drasticamente o custo dessas verificações, permitindo consultas em tempo constante.

Isso evita processamento redundante e melhora o desempenho em grafos grandes.

---

# 8. Algoritmos Utilizados

## 8.1 Detecção de Ciclos (DFS)

Implementada através de DFS (Depth First Search).

### Justificativa

O DFS foi escolhido porque:

- Possui implementação simples e eficiente.
- Percorre todas as dependências de forma natural.
- Detecta ciclos em uma única travessia do grafo.
- Apresenta excelente desempenho para grafos esparsos.

Durante a execução, o algoritmo mantém uma pilha de recursão. Caso um nó seja encontrado novamente dentro dessa pilha, existe uma dependência circular (deadloop).

### Complexidade

```text
O(n + m)
```

onde:

- n = tarefas
- m = dependências

---

## 8.2 Ordenação Topológica (Algoritmo de Kahn)

Implementada utilizando o algoritmo de Kahn.

### Justificativa

O algoritmo de Kahn foi escolhido porque:

- Produz diretamente uma sequência válida de execução.
- Detecta ciclos naturalmente.
- Possui complexidade linear.
- É amplamente utilizado em sistemas de gerenciamento de dependências.

Caso a quantidade de tarefas processadas seja menor que o total de tarefas do grafo, o algoritmo identifica automaticamente a existência de um ciclo.

### Complexidade

```text
O(n + m)
```

---

## 8.3 Construção da Árvore

Construída recursivamente a partir das raízes do grafo.

### Justificativa

A abordagem recursiva foi escolhida porque:

- Reflete naturalmente a estrutura hierárquica do problema.
- Simplifica a implementação.
- Facilita a geração das representações ASCII e JSON.
- Mantém boa legibilidade do código.

### Complexidade

```text
O(n + m)
```

---

## 8.4 Busca por Tarefas

Realizada através de tabelas hash indexadas por ID e nome.

### Justificativa

Essa estratégia foi escolhida para atender ao requisito não funcional de busca em tempo constante.

Sem indexação, seria necessário percorrer toda a lista de tarefas para cada consulta.

Com tabelas hash, a busca ocorre em:

```text
O(1)
```

independentemente da quantidade de tarefas cadastradas.

---

## 8.5 Geração de Estatísticas

As estatísticas da árvore são calculadas através de uma única passagem pelos dados.

### Justificativa

Foi adotada uma estratégia de passagem única para evitar múltiplas iterações sobre a estrutura de dados.

Isso reduz o custo computacional e mantém o processamento eficiente mesmo para grandes volumes de informações.

### Complexidade

```text
O(n + m)
```

---

# 9. Requisitos Funcionais Implementados

| Requisito | Implementado |
|------------|------------|
| RF-01 Leitura TXT/JSON | Sim |
| RF-02 Exportação TXT/JSON | Sim |
| RF-03 Construção da árvore | Sim |
| RF-04 Detecção de deadloop | Sim |
| RF-05 Menu CLI | Sim |
| RF-06 Comando via terminal | Sim |
| RF-07 Visualização ASCII | Sim |
| RF-08 Estatísticas da árvore | Sim |
| RF-09 Informações de task | Sim |
| RF-10 Busca por ID ou nome | Sim |
| RF-11 JSON String da árvore | Sim |
| RF-12 Ordem topológica | Sim |

---

# 10. Complexidade Computacional

| Operação | Complexidade |
|------------|------------|
| Busca por ID | O(1) |
| Busca por Nome | O(1) |
| Detecção de Ciclos | O(n + m) |
| Ordenação Topológica | O(n + m) |
| Construção da Árvore | O(n + m) |
| Estatísticas | O(n + m) |
| Exportação JSON | O(n + m) |

O requisito não funcional de busca em O(1) foi atendido por meio do uso de tabelas hash.

## Justificativa da Complexidade

Um dos objetivos do projeto foi garantir escalabilidade para grandes volumes de tarefas.

Por esse motivo foram priorizados algoritmos lineares ou quase lineares.

As operações mais custosas do sistema apresentam complexidade O(n + m), onde:

- n representa a quantidade de tarefas.
- m representa a quantidade de dependências.

Esse comportamento é considerado adequado para grafos de grande porte e permite processar milhares de tarefas sem crescimento exponencial do tempo de execução.

---

# 11. Teste de Estresse

## Objetivo

Validar o comportamento do sistema sob carga massiva.

---

## Cenário

Arquivo gerado automaticamente por:

```bash
python data/generate.py
```

Características:

| Métrica | Valor |
|----------|---------|
| Tarefas | 10.000 |
| Dependências | ~25.000 |
| Ciclo inserido | Sim |
| Tamanho do ciclo | 5 tarefas |

## Justificativa do Cenário

O teste de estresse foi desenvolvido para simular um ambiente significativamente maior do que os exemplos utilizados durante o desenvolvimento.

A escolha de:

- 10.000 tarefas
- aproximadamente 25.000 dependências

permite avaliar:

- Eficiência dos algoritmos.
- Consumo de memória.
- Escalabilidade das estruturas de dados.
- Robustez da detecção de ciclos.

Além disso, foi inserido propositalmente um ciclo envolvendo cinco tarefas para validar a capacidade do sistema de identificar deadloops em cenários complexos.

---

## Metodologia

O gerador cria:

1. Uma task raiz.
2. Múltiplos níveis hierárquicos.
3. Dependências aleatórias adicionais.
4. Um deadloop oculto envolvendo as últimas tarefas.

Esse cenário testa simultaneamente:

- Construção do grafo.
- Construção da árvore.
- Busca.
- Estatísticas.
- Ordenação topológica.
- Detecção de ciclos.

---

## Resultado Esperado

O sistema deve:

- Processar as 10.000 tarefas.
- Processar aproximadamente 25.000 dependências.
- Detectar corretamente o deadloop inserido.
- Impedir a geração de uma ordem topológica inválida.
- Retornar mensagem clara de erro.

## Relevância do Teste

Esse cenário exerce carga simultânea sobre praticamente todos os componentes do sistema:

- Leitura de arquivos.
- Construção do grafo.
- Detecção de ciclos.
- Ordenação topológica.
- Construção da árvore.
- Busca.
- Exportação.

Dessa forma, os resultados obtidos fornecem evidências de que a solução mantém comportamento correto mesmo sob grandes volumes de dados.

---

# 12. Requisitos Não Funcionais Atendidos

| Requisito | Situação |
|------------|------------|
| Compatível com Windows | Atendido |
| Compatível com Linux/Unix | Atendido |
| Busca O(1) | Atendido |
| Estruturas próprias | Atendido |
| Sem NetworkX | Atendido |
| Tolerância a erros | Atendido |

---

# 13. Conclusão

O ThreadFlow_Task atende integralmente os requisitos funcionais e não funcionais especificados.

A utilização de estruturas próprias de grafos, árvores, tabelas hash e algoritmos clássicos permitiu implementar um sistema eficiente, escalável e independente de bibliotecas especializadas.

A implementação própria dessas estruturas, sem o uso de bibliotecas específicas de grafos, permitiu compreender e aplicar conceitos fundamentais de Estruturas de Dados e Algoritmos, incluindo grafos direcionados, árvores, DFS, ordenação topológica e análise de complexidade computacional.

Os testes de estresse com 10.000 tarefas e aproximadamente 25.000 dependências demonstram que a solução é capaz de lidar com grandes volumes de dados, mantendo a capacidade de detectar deadloops, gerar estatísticas e produzir representações estruturadas das dependências.
