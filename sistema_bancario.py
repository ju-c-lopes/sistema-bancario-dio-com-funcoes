from datetime import date
from os import system
import platform

if platform.system() == "Windows":
    system("cls")
else:
    system("clear")

ESTADOS = {
    "Acre": "AC",
    "Alagoas": "AL",
    "Amapá": "AP",
    "Amazonas": "AM",
    "Bahia": "BA",
    "Ceará": "CE",
    "Espírito Santo": "ES",
    "Goiás": "GO",
    "Maranhão": "MA",
    "Mato Grosso": "MT",
    "Mato Grosso do Sul": "MS",
    "Minas Gerais": "MG",
    "Pará": "PA",
    "Paraíba": "PB",
    "Paraná": "PR",
    "Pernambuco": "PE",
    "Piauí": "PI",
    "Rio de Janeiro": "RJ",
    "Rio Grande do Norte": "RN",
    "Rio Grande do Sul": "RS",
    "Rondônia": "RO",
    "Roraima": "RR",
    "Santa Catarina": "SC",
    "São Paulo": "SP",
    "Sergipe": "SE",
    "Tocantins": "TO",
}

ano_atual = date.today().year

def calcularBissexto(ano):
    if ano % 100 == 0 and ano % 400 == 0:
        return True
    elif ano % 4 == 0:
        return True
    return False

MESES_DIAS = {
    "01": 31,
    "02": 28,
    "03": 31,
    "04": 30,
    "05": 31,
    "06": 30,
    "07": 31,
    "08": 31,
    "09": 30,
    "10": 31,
    "11": 30,
    "12": 31,
}

header = f"""
    {"=" * 50}
    {"sistema bancário dio".upper().center(50, " ")}
    {"=" * 50}

"""
print(header)

nome_usuario = input("Nome do usuário: ")

print(f"Seja bem-vindo(a) {nome_usuario.title()} ao {'sistema bancário dio'.upper()}!!!")

# Variáveis

usuarios = []
contas = []
saque_acumulado = 0
limite_saque = 500
quantidade_saques = 0

def verificar_data(data):
    validacao = data.split("/") if data.find("/") != -1 else data.split("-")
    try:
        bissexto = calcularBissexto(int(validacao[2]))
        if bissexto and validacao[1] == "02":
            dia_invalido = int(validacao[0]) > int(MESES_DIAS.get(validacao[1], -1) + 1)
        else:
            dia_invalido = int(validacao[0]) > int(MESES_DIAS.get(validacao[1], -1))
        if \
            len(validacao) != 3 or \
            len(validacao[2]) != 4 or \
            len(validacao[0]) != 2 or \
            len(validacao[1]) != 2 or \
            (ano_atual - int(validacao[2])) < 18 or \
            dia_invalido:
            if (ano_atual - int(validacao[2])) < 18:
                print("Para abrir uma conta você deve ser maior de 18 anos de idade!")
                return "Menor de idade"
            print("""
                \rData inválida!
                \rO formato deve ser "dd/mm/yyyy" ou "dd-mm-yyyy", onde:
                    \r\tdd = dia (2 caracteres)
                    \r\tmm = mês (2 caracteres)
                    \r\tyyyy = ano (4 caracteres)
                \rDigite-a novamente: """, end="")
            entrada = input()
            verificar_data(entrada)
    except IndexError:
        data = input("Data inválida! Digite-a novamente: ")
        verificar_data(data)
    return data

def filter_cpf(clientes, numero_cpf):
    def checar_clientes(cliente):
        for valores in cliente.values():
            if numero_cpf in valores:
                return True
        return False
    return filter(checar_clientes, clientes)

def filter_conta(contas_bancarias, numero_cpf):
    def checar_contas(conta):
        for valores in conta["usuario"].values():
            if numero_cpf in valores:
                return True
        return False
    return filter(checar_contas, contas_bancarias)

def cadastrar_usuario():
    usuario = {}
    usuario["nome"] = input("Digite seu nome completo: ")
    data_nascimento = input("Digite sua data de nascimento: ")
    data_nascimento = verificar_data(data_nascimento)
    if data_nascimento == "Menor de idade":
        return data_nascimento
    usuario["data_nascimento"] = data_nascimento
    try:
        cpf_informado = input("Digite seu CPF: ")
        while True:
            while len(cpf_informado) != 11:
                cpf_informado = input("Seu CPF é inválido, digite-o novamente: ")
            cpfs = list(filter_cpf(usuarios, cpf_informado))
            if cpfs:
                cpf_informado = input("CPF já cadastrado! Cadastre um novo CPF ou digite \"S\" para sair: ")
                if cpf_informado.lower() == "s":
                    return "sair"
            else:
                break
        usuario["CPF"] = cpf_informado
    except ValueError:
        print("Seu CPF deve conter apenas números.")
        cadastrar_usuario()
    logradouro = input("Digite a rua/avenida da sua residência: ")
    numero_residencia = input("Digite o número da sua residência: ")
    bairro = input("Digite o bairro onde você reside: ")
    cidade = input("Digite a cidade onde você reside: ")
    estado = input("Digite o estado em que você reside: ")
    sigla = ""
    while estado.title() not in ESTADOS.keys() and estado.upper() not in ESTADOS.values():
        estado = input("O estado que você forneceu é inválido, digite novamente: ")
        print(ESTADOS.keys())
    if estado.title() in ESTADOS.keys():
        estado = estado.title()
        sigla = ESTADOS[estado.title()]
    elif estado.upper() in ESTADOS.values():
        sigla = estado.upper()
        for e, s in ESTADOS.items():
            if sigla == s:
                estado = e.title()
    usuario["endereco"] = f"{logradouro.title()}, {numero_residencia} - {bairro}-{cidade}/{sigla} {estado}"
    return usuario

def cadastrar_conta():
    conta = {
        "agência": "0001",
        "número": f"{len(contas) + 1}",
        "saldo": 0,
        "extrato": f"""
            \r{'extrato'.upper()}
            \r{"-" * 30}\n"""}
    cpf_conta = input("Digite o CPF do cliente: ")
    usuario = list(filter_cpf(usuarios, cpf_conta))
    if not usuario:
        return "Usuário não encontrado."
    conta["usuario"] = usuario[0]
    return conta

def efetuar_deposito(saldo, valor_depositado, extrato):
    if extrato.find("movimentação") != -1:
        extrato = f"""
            \r{'extrato'.upper()}
            \r{"-" * 30}\n"""
    if valor_depositado <= 0:
        return "Depósitos devem ser maiores que 0(zero)"
    saldo += valor_depositado
    entrada = f"\n\rDepósito de R$ {valor_depositado:.2f}\n{'-' * 30}"
    extrato += entrada
    return saldo, extrato

def efetuar_saque(*, saldo, valor, extrato, limite_saque, quantidade_saques, saque_acumulado):
    if extrato.find("movimentação") != -1:
        extrato = f"""
            \r{'extrato'.upper()}
            \r{"-" * 30}\n"""
    if saldo <= 0:
        return "Você não tem saldo em conta para realizar operação de saque!"
    if quantidade_saques >= 3:
        return f"{'-' * 30}\nVocê excedeu a quantidade diária permitida para realizar saques.\n{'-' * 30}"
    if saque_acumulado + valor > limite_saque or valor > limite_saque:
        return f"{'-' * 30}\nO limite diário para saque é de R$ {limite_saque:.2f}\n{'-' * 30}"
    if valor > saldo:
        return f"O valor do saque de R$ {valor:.2f} excede seu saldo de R$ {saldo:.2f}"
    saldo -= valor
    saque_acumulado += valor
    quantidade_saques += 1
    saida = f"\n\rSaque de R$ {valor:.2f}\n{'-' * 30}"
    extrato += saida
    return saldo, extrato, quantidade_saques, saque_acumulado

def mostrar_extrato(saldo, *, extrato):
    if extrato.find("Depósito") == -1 and extrato.find("Saque") == -1:
        if extrato.find("movimentação") == -1:
            extrato += "Sem movimentação na conta"
    mensagem = f"{'-' * 30}\nSaldo atual: R$ {saldo:.2f}\n{'-' * 30}"
    return extrato, mensagem

def buscar_conta():
    cpf_informado = input("Digite seu CPF: ")
    contas_buscadas = list(filter_conta(contas, cpf_informado))
    conta = contas_buscadas[0]
    return conta

while True:
    menu = """
    Qual operação deseja fazer?
    
    [1] Cadastrar cliente
    [2] Cadastrar conta
    [3] Depósito
    [4] Saque
    [5] Extrato
    [6] Ver conta
    [7] Sair
    """

    mensagem = ""

    # ======================== DISPLAY MENU =============================
    print(menu)
    try:
        opcao = int(input("\tDigite sua opção: "))
        if opcao != 3 and extrato.find("movimentação") != -1:
            extrato = f"""
            \r{'extrato'.upper()}
            \r{"-" * 30}
            \r"""
    except ValueError:
        print(f"\nO valor digitado não é válido.\n")
        continue
    print()

    # ======================= Opção inválida ============================
    if opcao not in range(1, 8):
        print("\nVocê digitou uma opção inválida!")
        continue

    # ====================== Cadastrar cliente ==========================
    elif opcao == 1:
        usuario = cadastrar_usuario()
        if usuario == "Menor de idade" or usuario == "sair":
            print("\nObrigado por utilizar nossos serviços!!!")
            break
        usuarios.append(usuario)
        mensagem = " Cadastro realizado com sucesso! ".center(50, "=")

    # ======================= Cadastrar conta ===========================
    elif opcao == 2:
        conta = cadastrar_conta()
        if conta == "Usuário não encontrado.":
            print("O cadastro não pôde ser feito.")
            continue
        contas.append(conta)
        mensagem = " Conta cadastrada com sucesso! ".center(50, "=")

    # ====================== Opção de depósito ==========================
    elif opcao == 3:
        conta_a_depositar = buscar_conta()
        valor_a_depositar = int(input("Digite a quantia que deseja depositar: "))
        
        retorno = efetuar_deposito(conta_a_depositar["saldo"], valor_a_depositar, conta_a_depositar["extrato"])
        conta_a_depositar["saldo"] = retorno[0]
        conta_a_depositar["extrato"] = retorno[1]
        mensagem = " Deposito feito com sucesso! ".center(50, "=")
        mensagem += f"""\n\r{'-' * 30}\nSaldo atual: R$ {conta_a_depositar["saldo"]:.2f}\n{'-' * 30}"""

    #  ====================== Opção de saque ============================
    elif opcao == 4:
        conta = buscar_conta()
        valor_do_saque = int(input("Digite o valor a sacar: "))
        retorno = efetuar_saque(
            saldo=conta["saldo"],
            valor=valor_do_saque,
            extrato=conta["extrato"],
            limite_saque=limite_saque,
            quantidade_saques=quantidade_saques,
            saque_acumulado=saque_acumulado)
        if isinstance(retorno, str):
            mensagem = retorno
        else:
            conta["saldo"] = retorno[0]
            conta["extrato"] = retorno[1]
            quantidade_saques = retorno[2]
            saque_acumulado = retorno[3]
            mensagem = " Saque realizado com sucesso! ".center(50, "=")
            mensagem += f"""\n\r{'-' * 30}\nSaldo atual: R$ {conta_a_depositar["saldo"]:.2f}\n{'-' * 30}"""

    #  ====================== Mostrar Extrato ===========================
    elif opcao == 5:
        conta = buscar_conta()
        print(conta["extrato"])
        retorno = mostrar_extrato(conta["saldo"], extrato=conta["extrato"])
        conta["extrato"] = retorno[0]
        mensagem = conta["extrato"]
        mensagem += "\n" + retorno[1]

    #  ========================= Ver Conta ==============================
    elif opcao == 6:
        conta = buscar_conta()
        mensagem = f"""
            \r{'-' * 30} CONTA {'-' * 30}
            \rAgência: {conta["agência"]}
            \rConta : {conta["número"]}
            \rUsuário:
            \r\tNome: {conta["usuario"]["nome"]}
            \r\tCPF: {conta["usuario"]["CPF"]}
            \r{'-' * 30}\nSaldo atual: R$ {conta["saldo"]:.2f}\n{'-' * 30}
        """

    #  ========================= Finalizar ==============================
    elif opcao == 7:
        print("\nObrigado por utilizar nossos serviços!!!")
        break

    if platform.system() == "Windows":
        system("cls")
    else:
        system("clear")

    print(header)

    if mensagem:
        print(mensagem)
    