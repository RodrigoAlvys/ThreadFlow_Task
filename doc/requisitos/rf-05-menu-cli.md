# Menu CLI
**ID:** RF-05  
**Responsável:** Rodrigo Alves  

---

## Descrição
Interface via linha de comando que oferece um menu interativo para o usuário acessar todas as funcionalidades do sistema (importar, exportar, buscar task, exibir árvore, etc.).

## Regras De Negócio
- O menu deve ser exibido quando o programa for executado sem argumentos
- Deve permitir navegação por opções numeradas
- Deve tratar entradas inválidas

## Requisitos Não Funcionais
- Compatível com Windows e Unix
- Feedback claro para cada ação

## Critérios de Aceite
- [ ] **CA1:** Menu é exibido ao executar `threadflow` sem argumentos
- [ ] **CA2:** Opção para sair do programa
- [ ] **CA3:** Cada funcionalidade (RF-01 a RF-12) é acessível via menu