import pandas as pd
import uuid
from datetime import datetime
from banco import criar_conexao , criar_tabelas

#partes dos clientes 

def cadastrar_clientes(conn):
    print("Para uma melhor experiencia , cadastre seus dados")
    nome = input("Qual o seu nome?: ")
    cpf = input("Digite seu CPF:")
    telefone = input("Digite seu número de telefone: ")
    email = input("Digite o seu EMAIL:")
    id_cliente = str(uuid.uuid4())
    
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Clientes (id, nome, cpf, telefone, email)
        VALUES (?, ?, ?, ?, ?)
    """, (id_cliente, nome, cpf, telefone, email))

    conn.commit()
    print("Cliente cadastrado com sucesso!")

#cadastro de produtos  
def cadastrar_produtos(conn):
    nome = input("Nome do Produto: ")
    categoria = input("Categoria do Produto: ")
    
    try:
        quantidade = int(input("Quantidade de Produtos: "))
        valor = float(input("Valor do Produto: "))
    except ValueError:
        print("Quantidade deve ser número inteiro e valor deve ser número.")
        return
    id_produto = str(uuid.uuid4())

    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Produto (id, categoria, nome, quantidade_estoque, valor)
        VALUES (?, ?, ?, ?, ?)
    """, (id_produto, categoria, nome, quantidade, valor))

    conn.commit()
    print("Produto cadastrado com sucesso!")

#vendas 

def realizar_venda(conn):
    cliente_id = input("Digite o ID do cliente: ")
    produto_id = input("Digite o ID do produto: ")
    quantidade = int(input("Quantidade: "))
    forma_pagamento = input("Forma de pagamento: ")

    venda_id = str(uuid.uuid4())
    item_id = str(uuid.uuid4())

    cursor = conn.cursor()

    # pegar valor do produto
    cursor.execute("SELECT valor FROM Produto WHERE id = ?", (produto_id,))
    resultado = cursor.fetchone()

    if not resultado:
        print("Produto não encontrado.")
        return

    valor_unitario = resultado[0]
    valor_total = valor_unitario * quantidade

    
    cursor.execute("""
        INSERT INTO Vendas (id, cliente_id, data, forma_pagamento, status, valor_total)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        venda_id,
        cliente_id,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        forma_pagamento,
        "concluida",
        valor_total
    ))

    
    cursor.execute("""
        INSERT INTO Itens_Venda (id, venda_id, produto_id, quantidade, valor_unitario)
        VALUES (?, ?, ?, ?, ?)
    """, (
        item_id,
        venda_id,
        produto_id,
        quantidade,
        valor_unitario
    ))

    conn.commit()
    print("Venda realizada com sucesso!")

def exportar_tabela_csv(conn, nome_tabela):
    df = pd.read_sql_query(f"SELECT * FROM {nome_tabela}", conn)
    df.to_csv(f"{nome_tabela}.csv", index=False)
    print(f"Tabela {nome_tabela} exportada para CSV com sucesso!")

def exportar_tudo(conn):
    tabelas = ["Clientes", "Produto", "Vendas", "Itens_Venda"]

    for tabela in tabelas:
        df = pd.read_sql_query(f"SELECT * FROM {tabela}", conn)
        df.to_csv(f"{tabela}.csv", index=False)
    print("Todas as tabelas exportadas!")

def excluir_produto(conn):
    nome = input("Digite o nome do produto que deseja excluir: ")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Produto WHERE nome = ?", (nome,))
    
    conn.commit()
    if cursor.rowcount > 0:
        print("Produto excluído com sucesso!")
    else:
        print("Produto não encontrado.")

def menu():
    conn = criar_conexao()
    criar_tabelas(conn)

    while True:
        print("\n--- MENU ---")
        print("1 - Cadastrar Cliente")
        print("2 - Cadastrar Produto")
        print("3 - Realizar Venda")
        print("4 - Sair")
        print("5 - Exportar banco para CSV")
        print("6 - Excluir Produto")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            cadastrar_clientes(conn)

        elif opcao == "2":
            cadastrar_produtos(conn)

        elif opcao == "3":
            realizar_venda(conn)

        elif opcao == "4":
            print("Encerrando sistema...")
            break
        elif opcao == "5":
            exportar_tudo(conn)
        elif opcao == "6":
                excluir_produto(conn)

        else:
            print("Opção inválida!")

    conn.close()

menu()   

