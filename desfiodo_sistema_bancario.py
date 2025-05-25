import textwrap

def menu():
    menu = """\n
    _________________menu_________________
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc]\tNova conta
    [lc]\tListar contas
    [nu]\tNovo usuário
    [q]\tSair
    => """
    return input(textwrap.dedent(menu))


def depositar(saldo, valor, extrato, /):
    if valor > 0:
        saldo += valor
        extrato += f"Depósito:\tR$ {valor:.2f}\n"
        print("\n Depósito realizado com sucesso!")
    else:
        print("\n O valor informado é invalido.\n por gentileza verifique o valor do deposito e tente novamente")    

    return saldo, extrato    

def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques > limite_saques

    if excedeu_saldo:
        print("\n Você não possui saldo suficente,\n verifique o valor e tente novamente!")
    elif excedeu_limite:
        print("\n O valor do saque excedeu o limite!, por gentileza altere o valor maximo de cada saque no app.")    
    elif excedeu_saques:
         print("\n O valor do saque excedeu o limite de saques diario, altere o limite de saques no app.")      
    elif valor > 0:
        saldo -= valor
        extrato += f"Saque:\t\tR$ {valor:.2f}\n"     
        numero_saques += 1
        print("\n Saque realizado com sucesso!")

    else:
        print("\n Operação falhou! Valor invalido, tente novamente.")    
    return saldo, extrato    

def exibir_estrato(saldo, /, *, extrato):
    print("\n================ Extrato ================")
    print("Não forram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo:\t\tR$ {saldo:.2f}")
    print("_________________________________")

def criar_usuario(usuarios):
    cpf = input("Informe o CPF (somente os números): ")
    usuario = filtrar_usuario(cpf, usuarios)  

    if usuario:
        print("\nJá existe um usuário com esse CPF!")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, número - bairro - cidade/UF): ")

    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})  

    print("Usuário criado com sucesso!")

def filtrar_usuario(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None

def criar_conta(agencia, numero_conta, usuarios):
    cpf = input("Informe o CPF do usuário: ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\nConta criada com sucesso!")
        return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}
    print("usuario não encontrado!\n por gentileza verifique e tente novamente.")

def listar_contas(contas):
    if len(contas) == 0:  # Se não houver contas, exibe a mensagem
        print("Ainda não há cadastro de contas.")
        return
    for conta in contas:
        Linha = f"""\
            Agência:\t{conta['agencia']}
            c/c:\t{conta['numero_conta']}
            titular:\t{conta['usuario']['nome']}

        """
        print("=" * 100)
        print(textwrap.dedent(Linha))
def main():
    LIMITE_SAQUES = 3
    AGENCIA = "0001"

    saldo = 0
    limite = 500
    extrato = ""
    numero_saque = 0
    usuarios = []
    contas = []
    numero_conta = 1
    while True:
        opcao = menu()

        if opcao == "d":
           valor = float(input("Por gentileza Informe o valor que deseja deposiar sem virgula:\n esse caixa não aceita centavos R$"))
           saldo, extrato = depositar(saldo, valor, extrato) 

        elif opcao == "s":
            valor = float(input("Por gentileza informe o valor do saque:\n R$"))

            saldo, extrato = sacar(
                saldo=saldo,
                valor=valor,
                extrato=extrato,
                limite=limite,
                numero_saques=numero_saque,
                limite_saques=LIMITE_SAQUES,
            )
        elif opcao == "e":
            exibir_estrato(saldo, extrato=extrato)

        elif opcao == "nu":
            criar_usuario(usuarios)

        elif opcao == "nc":
            # numero_conta = len(contas) + 1 
            conta = criar_conta(AGENCIA, numero_conta, usuarios)

            if conta:
                contas.append(conta)
                numero_conta += 1 # para uma futura implementação de remover conta sem gerar erro de id
        elif opcao == "lc":
            listar_contas(contas)        

        elif opcao == "q":
            break

        else:
            print("Operação inválida, por gentileza selecinar novamente a operação desejada.")

main()