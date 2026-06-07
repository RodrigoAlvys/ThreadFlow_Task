# Comando via Terminal
**ID:** RF-06  
**Responsável:** Luiz Arthur  

---

## Descrição
Permite executar o fluxo completo do programa via um único comando no terminal, com parâmetros de entrada e saída.

## Regras De Negócio
- Formato: `threadflow --if=<arquivo_entrada> --of=<arquivo_saida>`
- O argumento `--if` define o arquivo de entrada (`.txt` ou `.json`)
- O argumento `--of` define o arquivo de saída (`.txt` ou `.json`)

## Requisitos Não Funcionais
- Deve funcionar em bash (Linux/Mac) e PowerShell/cmd (Windows)
- Tratamento de erros (arquivo não encontrado, formato inválido)

## Critérios de Aceite
- [ ] **CA1:** Comando com `--if` e `--of` executa leitura, ordenação e exportação
- [ ] **CA2:** Retorna erro se `--if` não existir
- [ ] **CA3:** Retorna erro se `--of` tiver extensão inválida