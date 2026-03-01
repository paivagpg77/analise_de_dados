import sqlite3

def criar_conexao():
    conn = sqlite3.connect("cinefilmes.db")
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def criar_tabelas(conn):
    cursor = conn.cursor()

    cursor.executescript("""
    CREATE TABLE IF NOT EXISTS Usuario (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE
    );


    CREATE TABLE IF NOT EXISTS Filme (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome_filme TEXT NOT NULL,
        ano INTEGER NOT NULL,
        genero TEXT NOT NULL
    );


    CREATE TABLE IF NOT EXISTS Avaliacao (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_usuario INTEGER NOT NULL,
        id_filme INTEGER NOT NULL,
        nota INTEGER NOT NULL CHECK(nota >= 0 AND nota <= 10),
        comentario TEXT,
        data_avaliacao DATE NOT NULL,

        FOREIGN KEY (id_usuario) REFERENCES Usuario(id) ON DELETE CASCADE,
        FOREIGN KEY (id_filme) REFERENCES Filme(id) ON DELETE CASCADE,
        UNIQUE (id_usuario, id_filme)
    );
    """)
    conn.commit()
