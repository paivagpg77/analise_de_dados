import uuid
from datetime import datetime
from banco import criar_conexao,criar_tabelas
import sqlite3
import pandas as pd

def cadastro_usuario(conn):
    print("Seja Bem-vindo, Faça seu cadastro aqui em baixo")
    nome = input("Digite seu nome: ")
    email = input("Digite seu gmail: ")

    cursor = conn.cursor()
    try:
        cursor.execute("""
        INSERT INTO Usuario ( nome , email)
        VALUES (?,?)""", 
        (nome, email))
        conn.commit()
        print("Cadastrado com Sucesso!")
    except sqlite3.IntegrityError:
        print("ERRO!: Esse Email já está cadastrado!")


def cadastro_filmes(conn):
    print("Responda os seguintes dados para cadastrar um filme!")
    nome_filme = input("Digite o nome do Filme: ")
    data_lancamento  =  int(input(f"Digte o Ano de {nome_filme}: "))
    genero = input(f"Digite o Gênero do fime {nome_filme}:")

    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO Filme (nome_filme ,ano ,genero)
        VALUES (?,?,?)''', (nome_filme,data_lancamento,genero))
    conn.commit()
    print("Filme Cadastrado com Sucesso!")   

def avaliar_filme(conn):
    cursor = conn.cursor()

    try:
        id_usuario = int(input("Digte o ID do Usuário: "))
        id_filme = int(input("Digite o ID do Filme: "))
        nota = int(input(f"Digite uma nota de 0 a 5 Para o Filme: "))

        if nota < 0 or nota > 5:
            print("A NOTA ESTÁ ENTRE 0 E 5!")
            return 
    except ValueError:
        print("ERRO!: Você deve digitar apenas números: ")
        return
    
    comentario = input("Digite um comentário: ")
    data_atual = data_atual = datetime.now().strftime("%Y-%m-%d")

    cursor.execute('''
        SELECT  id_usuario  FROM Avaliacao 
        WHERE id_usuario = ? AND id_filme = ?''',
        (id_usuario, id_filme))
    resultado = cursor.fetchone()

    if resultado:
        cursor.execute('''
            UPDATE Avaliacao
            SET nota = ? , comentario = ? , data_avaliacao = ?
            WHERE id_usuario = ? AND id_filme = ? ''', 
            (nota , comentario , data_atual , id_usuario , id_filme))
        print("Avaliação atualizada com sucesso!")

    else:
        cursor.execute('''
            INSERT INTO Avaliacao (id_usuario , id_filme , nota , comentario , data_avaliacao)
            VALUES (?,?,?,?,?)''',
            (id_usuario , id_filme , nota,  comentario, data_atual))
        print("Avaliação cadastrada com sucesso!")    

    conn.commit()       

def exportar_tabelas(conn):
    conn = sqlite3.connect("cinefilmes.db")

    tabelas = ["Usuario", "Filme", "Avaliacao"]

    for tabela in tabelas:
        df = pd.read_sql_query(f"SELECT * FROM {tabela}", conn)
        df.to_csv(f"{tabela}.csv", index=False, encoding="utf-8")
        print(f"Tabela {tabela} exportada com sucesso!")




def menu():
    conn = criar_conexao()
    criar_tabelas(conn)

    while True:
        print("\n=== CINEFILMES ===")
        print("1 - Cadastrar usuário")
        print("2 - Cadastrar filme")
        print("3 - Avaliar filme")
        print("4 - Sair")
        print("5 - Exportar tabela CSV")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            cadastro_usuario(conn)

        elif opcao == "2":
            cadastro_filmes(conn)

        elif opcao == "3":
            avaliar_filme(conn)

        elif opcao == "4":
            print("Encerrando sistema...")
            conn.close()
            break
        elif opcao == '5':
            exportar_tabelas(conn)
        else:
            print("Opção inválida!")

if __name__ == "__main__":
    menu()