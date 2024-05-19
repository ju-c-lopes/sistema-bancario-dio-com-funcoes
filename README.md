# Otimização de Sistema Bancário DIO

Desafio de Otimização da primeira versão do Sistema Bancário DIO usando funções Python

A primeira versão do projeto pode ser acessada [aqui](https://github.com/ju-c-lopes/sistema-bancario-dio).

---

## Requisitos

---

### Objetivos Gerais

---

#### Separar funcionalidades existentes em funções Python para:

1. Saque
    * A função saque deve receber os argumentos apenas por nome
        #### Sugestão

        - saldo
        - valor
        - extrato
        - limite
        - numero_saques
        - limite_saques

        #### Retorno

        - Saldo
        - Extrato

2. Depósito
    * A função depósito deve receber argumentos apenas por posição
        #### Sugestão

        - saldo
        - valor
        - extrato

        #### Retorno
        - Saldo
        - Extrato

3. Extrato
    * A função extrato deve receber argumentos por posição e nome
        #### Sugestões
        - saldo (argumento posicional)
        - extrato (argumento nomeado)

#### Criar novas funções para:

1. Cadastro de usuário/cliente
    * O programa deve armazenar os usuários em uma lista
    * Um usuário é composto por:
        - nome
        - data de nascimento
        - CPF
            * Deve ser armazenado somente os 11 números do CPF
            * Não pode ser possível cadastrar 2 usuários com o mesmo CPF
        - endereço
            * O endereço é uma string com o formato:
            "{logradouro}, {n°} - {bairro} - {cidade}/{sigla} {estado}"

2. Cadastrar conta bancária
    * O programa deve armazenar contas em uma lista
    * Uma conta é composta por:
        - Agência
            * O número da agência é fixo: "0001"
        - Número da conta
            * O número da conta é sequencial, iniciando por 1
            * Uma conta deve pertencer somente a 1 usuário
        - Usuário
            * O usuário pode ter mais de uma conta

##### Opcional
3. Listar Contas
4. Listar Usuários
5. Inativar Conta

---
### DICA
---
* Para vincular um usuário a uma conta, filtre a lista de usuários buscando o número do CPF informado para cada usuário da lista.
