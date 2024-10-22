from datetime import datetime
from abc import ABC, abstractmethod


menu = """
[u]  Criar usuario          [d]  Depositar
[c]  Criar conta            [s]  Sacar
[lu] Listar usuarios        [e]  Extrato
[lc] Listar contas          [q] Sair

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


class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)

    @property
    def saldo(self):
        return self._saldo
    
    @property
    def numero(self):
        return self._numero
    
    @property
    def agencia(self):
        return self._agencia
    
    @property
    def historico(self):
        return self._historico
    
    def sacar(self, valor):
        saldo = self.saldo
        excedeu_saldo = valor > saldo

        if excedeu_saldo:
            print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")

        elif valor > 0:
            self._saldo -= valor
            print("\n=== Saque realizado com sucesso! ===")
            return True

        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")

        return False

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("\n=== Depósito realizado com sucesso! ===")
        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
            return False

        return True
    
    @staticmethod
    def exibir_extrato(transacoes):
        for transacao_dict in transacoes:
            for chave, valor in transacao_dict.items():
                print(f"{chave}: {valor}")

    def gerar_extrato(self):
        print("\n================ EXTRATO ================")
        print("Não foram realizadas movimentações.") if not self._historico.transacoes else self.exibir_extrato(self._historico.transacoes)
        print(f"\nSaldo: R$ {self.saldo:.2f}")
        print("==========================================")

    def __str__(self):
        return f"""\
            Titular:\t{self._cliente.nome}
            Agência:\t{self.agencia}
            Numero:\t{self.numero}
            Saldo:\t{self.saldo}
        """

class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques

    def sacar(self, valor):
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__]
        )

        excedeu_limite = valor > self.limite
        excedeu_saques = numero_saques >= self.limite_saques

        if excedeu_limite:
            print("\n@@@ Operação falhou! O valor do saque excede o limite. @@@")

        elif excedeu_saques:
            print("\n@@@ Operação falhou! Número máximo de saques excedido. @@@")

        else:
            return super().sacar(valor)

        return False


class Cliente:
    def __init__(self, endereco):
        self._endereco = endereco
        self._contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self._contas.append(conta)
    
    def obter_qtdd_contas(self):
        return self._contas
    
    def obter_conta(self, num):
        for conta in self._contas:
            if conta.numero == num:
                return conta
        print("O Cliente informado não tem conta com esse número")
        return None
    
    def listar_contas(self):
        if not self._contas:
            print("Nenhuma conta foi criada ainda.")
            return
        
        print()
        for conta in self._contas:
            print(conta)

class PessoaFisica(Cliente):
    def __init__(self, cpf, nome, data_nascimento, endereco):
        super().__init__(endereco)
        self._cpf = cpf
        self._nome = nome
        self._data_nascimento = data_nascimento
    
    @property
    def cpf(self):
        return self._cpf
    
    @property
    def nome(self):
        return self._nome
    
    def __str__(self):
        return f"Nome: {self._nome}\n\
            CPF: {self.cpf}\n\
            Nascimento: {self._data_nascimento:%d-%m-%Y}\n\
            Endereco: {self._endereco}"


class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d/%m/%Y, %H:%M:%S"),
            }
        )


class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass

    @classmethod
    @abstractmethod
    def registrar(self, conta):
        pass


class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


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
    for pessoa in usuarios:
        if pessoa.cpf == cpf:
            return True
    return False

def criar_usuario(usuarios):

    cpf = input("Digite o cpf (numeros apenas): ")
    if(verifica_se_usuario_existe(usuarios, cpf)):
        print("\nO usuario com o CPF fornecido ja existe!")
        print("Operacao cancelada.")
        return

    nome = input("Digite o nome do novo usuario: ")

    try:
        data_nascimento = datetime.strptime(input("Digite a data de nascimento (dd/mm/aaaa): "), "%d/%m/%Y")
    except ValueError:
        print("A data digitada naão confere com o formato requisitado")
        print("Operacao cancelada.")
        return
    
    endereco = input("Digite o endereco (logradouro, num - bairro - cidade/siglaEstado): ")

    usuarios.append(PessoaFisica(cpf, nome, data_nascimento, endereco))
    print(f"Usuario de cpf {cpf} foi inserido no sistema!")

    return

def encontrar_usuario_por_cpf(usuarios, cpf):
    for pessoa in usuarios:
        if pessoa.cpf == cpf:
            return pessoa
    print("Não há usuario com esse cpf")
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

def listar_usuarios(usuarios):
    if not usuarios:
        print("Nenhum usuario foi criado ainda.")
        return
    print()
    for usuario in usuarios:
        print(usuario)
        print()

def listar_contas(contas):
    if not contas:
        print("Nenhuma conta foi criada ainda.")
        return
    print()
    for conta in contas:
        agencia, num, usuario = conta.values()
        cpf = usuario["cpf"]
        print(f"conta {num}:")
        print(f"agencia - {agencia}")
        print(f"cpf do usuario - {cpf}\n")

    
def input_cpf_para_usuario():
    cpf = input("Digite o cpf do usuario:\t")
    return encontrar_usuario_por_cpf(usuarios, cpf)

def input_para_conta():
    usuario: PessoaFisica = input_cpf_para_usuario()
    if usuario:
        num_conta = int(input("Digite o numero da conta:\t"))
        return usuario.obter_conta(num_conta)

while True:

    opcao = input(menu).lower()

    match opcao:
        case "u" | "criar usuario":
            criar_usuario(usuarios)
        
        case "lu" | "listar usuarios":
            listar_usuarios(usuarios)
        
        case "c" | "criar conta":
            cpf = input("Digite o cpf do usuario:\t")
            usuario: PessoaFisica = encontrar_usuario_por_cpf(usuarios, cpf)
            if usuario:
                num = len(usuario.obter_qtdd_contas()) + 1
                usuario.adicionar_conta(ContaCorrente.nova_conta(usuario, num))
                print(f"Conta numero {num} criada com sucesso!")
        
        case "d" | "depositar":
            conta = input_para_conta()
            if conta:
                valor = float(input("Informe o valor do depósito: "))
                Deposito(valor).registrar(conta)
            
        case "s" | "sacar":
            conta = input_para_conta()
            if conta:
                valor = float(input("Informe o valor do saque: "))
                Saque(valor).registrar(conta)

        case "e" | "extrato":
            conta = input_para_conta()
            if conta:
                conta.gerar_extrato()
        
        case "lc" | "listar contas":
            cpf = input("Digite o cpf do usuario:\t")
            usuario: PessoaFisica = encontrar_usuario_por_cpf(usuarios, cpf)
            if usuario:
                usuario.listar_contas()
        
        case "q" | "sair":
            break
        
        case _:
            print("Operação inválida, por favor selecione novamente a operação desejada.")

        
