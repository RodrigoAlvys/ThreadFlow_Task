# Documento De Requisitos Do Produto
**Versão do documento:** 1.0
**Nome do projeto:** ThreadFlow_Task
**Público alvo:** Programadores, Agents Autônomos e empresas de tecnologia
**Proposta de valor:** Programa CLI que organiza tarefas dependentes em ordem topológica com detecção para *deadloop[^2]*
**Descrição:** Programa CLI que receberá uma lista de tarefas dependentes, seja em .txt ou .json, construindo uma árvore de dependências, retornando erro em caso de *deadloop[^2]* e exportando um arquivo .txt ou .json

---

## Stakeholders
|Nome         |Cargo|Responsabilidade           |
|-------------|:---:|---------------------------|
|Rodrigo Alves|PO   |Visão técnica e priorização|
|Luiz Arthur  |Dev  |Desenvolvedor fullstack    |
|Davi Souza   |Dev  |Desenvolvedor fullstack    |
>[!IMPORTANT]
>O *stakeholder* externo principal será o prof. Amaury Nogueira, que representa o cliente final e avaliará os resultados na apresentação.

## Escopo
### Dentro Do Escopo
- Organizar tarefas com menor dependências para o maior, topológica
- Detectar *deadloop[^2]*
- Importar arquivo .txt ou .json para receber listas de tarefas
- Exportar arquivo .txt. ou .json com lista ordenada.
- Interface CLI
- Comando via terminal

### Fora Do Escopo
- GUI completa
- Suporte direto para programas de terceiros
- Processar as tarefas
- Detectar *tasks* online automaticamente no sistema

## Regras De Negócio
- Proibido uso de bibliotecas de alto nível, exemplo: networkx[^1]
- Criação de estrutura de dados próprios
- Projeto deve funcionar via linha de comando
- Deve receber arquivo externo como entrada
- Deve exportar o resultado em formato de arquivo
- Documentação completa
- Organização de arquivos internos

## Requisitos Técnicos
- Python3.9+
- JSON

## Requisitos
### Requisitos Funcionais
- **RF-01:** Leitura de arquivo .txt e .json
- **RF-02:** Retornar resultado em .txt ou json
- **RF-03:** Construir árvore de requisitos
- **RF-04:** Detectar *deadloop[^2]*
- **RF-05:** Menu CLI
- **RF-06:** Comando via terminal, exemplo: `threadflow --if=foo.txt --of=fooo.json`
- **RF-07:** Demonstração visual da árvore em ASCII
- **RF-08:** Mostrar informações básicas e pertinentes da árvore, exemplo: números de tasks, números de dependência, task com mais dependências e task mais requisitada
- **RF-09:** Mostrar informações básicas específica de uma task
- **RF-10:** Procurar task através de id ou nome
- **RF-11:** Funcionalidade com retorno em string da árvore de requisitos

### Requisitos Não Funcionais
- Deve funcionar em sistema operacionais windows e unix
- Complexidade da árvore de dependência menor ou igual a Big $O(n \log n)$
- Complexidade de busca de tasks com id igual a Big $O(1)$
- Tolerância a erros

## Critérios de Aceite
- [ ] **CA-01:** O sistema lê arquivos de entrada nos formatos `.txt` e `.json`
- [ ] **CA-02:** O sistema exporta o resultado nos formatos `.txt` e `.json`
- [ ] **CA-03:** O sistema constrói corretamente a árvore de dependências a partir da entrada
- [ ] **CA-04:** O sistema detecta *deadloop[^2]* e retorna erro claro quando existem dependências circulares
- [ ] **CA-05:** O comando `threadflow --if=<entrada> --of=<saida>` executa o fluxo completo
- [ ] **CA-06:** O menu CLI é exibido e permite acesso a todas as funcionalidades
- [ ] **CA-07:** O sistema retorna a árvore de dependências em formato string via comando de terminal
- [ ] **CA-08:** O sistema exibe a árvore de dependências em formato ASCII no terminal
- [ ] **CA-09:** O sistema mostra informações resumidas da árvore: número de tasks, número de dependências, task com mais dependências e task mais requisitada
- [ ] **CA-10:** O sistema mostra informações detalhadas de uma task específica
- [ ] **CA-11:** O sistema permite buscar uma task por `id` ou `nome` e retorna seus dados

[^1]: Biblioteca de estrutura de dados pensando em grafos e visualização,[**link**](https://networkx.org/documentation/stable/index.html#) oficial do site.
[^2]: *Deadloop* são dependências cíclicas que ocorrem quando dois ou mais processos ficam bloqueados indefinidamente por dependerem mutuamente dos recursos que o outro possui, gerando um impasse.
