# Leitura de arquivo `.txt` e `.json`
**ID:** RF-01  
**Responsável:** Luiz Arthur  

---

## Descrição
Funcionalidade que ler arquivo `.txt` e `.json` com lista de task e suas dependências retornando um dicionário com tasks como chave e suas dependências como valor: `dic[str, list[str]]`.

## Regras De Negócio
- O arquivo `.txt` deve guardar listas de tarefas junto com suas dependências, cada task separado por ponto e vírgula, Exemplo: "task:nome_task, depen:task1, task2; task:nome_t..."
- O arquivo `.json` deve guardar dicionário com tasks como chave e dependências como conteúdo: `{"task_nome": ["task1", "task2", "task3", "task4"]}`

## Requisitos Não Funcionais
- Resistência a erros

## Critérios de Aceite
- [ ] **CA1:** Ler arquivos `.json` ou `.txt` estruturado e retornar dicionário com nome da task como key e lista de dependência como valor: `dic[str, list[str]]`
- [ ] **CA2:** Resistência a erro ao ler arquivo com formato errado ou conteúdo errado.