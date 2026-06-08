# Funcionalidade com Retorno em String JSON da Árvore de Requisitos
**ID:** RF-11  
**Responsável:** Davi Souza  

---

## Descrição
Permite obter uma representação completa do estado atual do sistema em formato JSON string, contendo a ordem topológica das tarefas e a estrutura da árvore de dependências. Útil para integração com outras ferramentas, logs ou APIs.

## Regras De Negócio
- O retorno deve ser uma string JSON válida
- Deve conter obrigatoriamente a ordem topológica e a representação da árvore
- Se houver *deadloop[^1]*, a ordem topológica deve vir vazia e o erro deve ser indicado no JSON
- Deve ser acessível via método público na API interna

## Requisitos Não Funcionais
- A geração do JSON deve ter complexidade $O(n + m)$
- Deve serializar corretamente caracteres especiais (escapamento UTF-8)

## Critérios de Aceite
- [ ] **CA1:** Chamar função e retorna string JSON válida
- [ ] **CA2:** Em caso de sucesso, o JSON contém ordem topológica e árvore
- [ ] **CA3:** Em caso de *deadloop[^1]*, ordem topológica é vazia e erro está presente no JSON
- [ ] **CA4:** O JSON pode ser desserializado sem erros

[^1]: Biblioteca de estrutura de dados pensando em grafos e visualização,[**link**](https://networkx.org/documentation/stable/index.html#) oficial do site.