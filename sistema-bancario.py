from datetime import datetime

menu = """

[d]  Depositar
[s]  Sacar
[e]  Extrato
[u]  Criar usuario
[c]  Criar conta
[q] Sair

=> """

saldo = 0
limite = 500
numero_saques = 0
proximo_num_conta = 1
LIMITE_SAQUES = 3
AGENCIA = "0001"
extrato = {}
usuarios = []
contas = []


def adiciona_operacao_com_tempo(dict, operacao):
    """Adiciona uma operacao ao dict, usando como chave o tempo atual"""
    tempo_agora = datetime.now()
    if dict.__contains__(tempo_agora):
        dict[tempo_agora].append(operacao)
    else:
        dict[tempo_agora] = [operacao]

def exibir_extrato(dict):
    for tempo, operacao in dict.items():
        print(f"{tempo:%d-%m-%Y %H:%M:%S} - {operacao}")

def sacar(*, valor, saldo, extrato, limite, numero_saques, limite_saques):
    
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= limite_saques

    if excedeu_saldo:
        print("Operação falhou! Você não tem saldo suficiente.")

    elif excedeu_limite:
        print("Operação falhou! O valor do saque excede o limite.")

    elif excedeu_saques:
        print("Operação falhou! Número máximo de saques excedido.")

    elif valor <= 0:
        print("Operação falhou! O valor informado é inválido.")

    else:
        saldo -= valor
        adiciona_operacao_com_tempo(extrato, f"Saque: R$ {valor:.2f}")
        numero_saques += 1
        print(f"Saque de R${valor:.2f} realizado")
        print(f"Saldo atualizado: R${saldo:.2f}")

    return saldo

def depositar(valor, saldo, extrato, /):
    if valor > 0:
        saldo += valor
        adiciona_operacao_com_tempo(extrato, f"Depósito: R$ {valor:.2f}")
        print(f"Deposito de R${valor:.2f} realizado")
        print(f"Saldo atualizado: R${saldo:.2f}")

    else:
        print("Operação falhou! O valor informado é inválido.")

    return saldo

def gerar_extrato(saldo, /, *, extrato):
    print("\n================ EXTRATO ================")
    print("Não foram realizadas movimentações.") if not extrato else exibir_extrato(extrato)
    print(f"\nSaldo: R$ {saldo:.2f}")
    print("==========================================")

def verifica_se_usuario_existe(usuarios, cpf):
    for user in usuarios:
        if user["cpf"] == cpf:
            return True
    return False

def criar_usuario(usuarios):

    cpf = int(input("Digite o cpf (numeros apenas): "))
    if(verifica_se_usuario_existe(usuarios, cpf)):
        print("\nO usuario com o CPF fornecido ja existe!")
        print("Operacao cancelada.")
        return

    nome = input("Digite o nome do novo usuario: ")

    try:
        data_nascimento = datetime.strptime(input("Digite a data de nascimento (dd/mm/aaaa): "), "%d/%m/%Y")
    except(ValueError):
    except ValueError:
        print("A data digitada naão confere com o formato requisitado")
        print("Operacao cancelada.")
        return
    
    endereco = input("Digite o endereco (logradouro, num - bairro - cidade/siglaEstado): ")

    usuarios.append({"nome": nome, "data_nascimento":data_nascimento, "cpf":cpf, "endereco": endereco})
    print(f"Usuario de cpf {cpf} foi inserido no sistema!")

    return

def encontrar_usuario_por_cpf(usuarios, cpf):
    for user in usuarios:
        if user["cpf"] == cpf:
            return user
    return None

def criar_conta(contas, agencia, num_conta, usuarios):
    """ Retorna o valor do proximo numero de conta """
    cpf = int(input("Digite o cpf do usuario ao qual a conta sera vinculada: "))
    usuario = encontrar_usuario_por_cpf(usuarios, cpf)
    if(not usuario):
        print("Nao existe usuario com esse CPF. Cancelando operacao.")
        return num_conta
    contas.append({"agencia":agencia, "num_conta":num_conta, "usuario":usuario})
    print("Conta criada com sucesso!")
    return num_conta + 1

    


while True:

    opcao = input(menu).lower()

    match opcao:
        case "d" | "depositar":
            valor = float(input("Informe o valor do depósito: "))
            saldo = depositar(valor, saldo, extrato)
            
        case "s" | "sacar":
            valor = float(input("Informe o valor do saque: "))
            saldo = sacar(valor=valor, saldo=saldo, extrato=extrato, limite=limite, numero_saques=numero_saques, limite_saques=LIMITE_SAQUES)

        case "e" | "extrato":
            gerar_extrato(saldo, extrato=extrato)
        
        case "u" | "criar usuario":
            criar_usuario(usuarios)

        case "c" | "criar conta":
            proximo_num_conta = criar_conta(contas, AGENCIA, proximo_num_conta, usuarios)
        
        case "q" | "sair":
            break
        
        case _:
            print("Operação inválida, por favor selecione novamente a operação desejada.")

        
