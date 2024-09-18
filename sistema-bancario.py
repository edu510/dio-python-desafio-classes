from datetime import datetime

menu = """

[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair

=> """

saldo = 0
limite = 500
extrato = {}
numero_saques = 0
LIMITE_SAQUES = 3


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
        print("Saldo atualizado: " + str(saldo))

    return saldo

def depositar(valor, saldo, extrato, /):
    if valor > 0:
        saldo += valor
        adiciona_operacao_com_tempo(extrato, f"Depósito: R$ {valor:.2f}")

    else:
        print("Operação falhou! O valor informado é inválido.")

    return saldo

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
            print("\n================ EXTRATO ================")
            print("Não foram realizadas movimentações.") if not extrato else exibir_extrato(extrato)
            print(f"\nSaldo: R$ {saldo:.2f}")
            print("==========================================")
        
        case "q" | "sair":
            break
        
        case _:
            print("Operação inválida, por favor selecione novamente a operação desejada.")

        
