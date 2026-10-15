import sqlite3
import json
import hashlib
from datetime import datetime

DB_PATH = "orcamentos.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Cria a tabela caso não exista
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orcamentos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            data_criacao TEXT NOT NULL,
            estado TEXT NOT NULL,
            dados_json TEXT NOT NULL,
            valor_total REAL NOT NULL
        )
    """)
    
    # Adiciona a coluna usuario_id se ela ainda não existir no banco antigo
    try:
        cursor.execute("ALTER TABLE orcamentos ADD COLUMN usuario_id INTEGER")
    except sqlite3.OperationalError:
        pass  # A coluna já existe, segue em frente
        
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            senha TEXT NOT NULL,
            plano TEXT DEFAULT 'Gratuito'
        )
    """)
    conn.commit()
    conn.close()

def hash_senha(senha: str) -> str:
    return hashlib.sha256(senha.encode()).hexdigest()

def cadastrar_usuario(nome: str, email: str, senha: str, plano: str = "Gratuito") -> bool:
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO usuarios (nome, email, senha, plano)
            VALUES (?, ?, ?, ?)
        """, (nome, email.lower().strip(), hash_senha(senha), plano))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False  # E-mail já cadastrado

def autenticar_usuario(email: str, senha: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, nome, email, plano FROM usuarios
        WHERE email = ? AND senha = ?
    """, (email.lower().strip(), hash_senha(senha)))
    user = cursor.fetchone()
    conn.close()
    
    if user:
        return {"id": user[0], "nome": user[1], "email": user[2], "plano": user[3]}
    return None

def salvar_orcamento(usuario_id: int, nome: str, estado: str, dados: list, valor_total: float) -> int:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    data_str = datetime.now().strftime("%d/%m/%Y %H:%M")
    dados_str = json.dumps(dados)
    cursor.execute("""
        INSERT INTO orcamentos (usuario_id, nome, data_criacao, estado, dados_json, valor_total)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (usuario_id, nome, data_str, estado, dados_str, valor_total))
    item_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return item_id

def listar_orcamentos(usuario_id: int = None) -> list:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    if usuario_id is not None:
        cursor.execute("""
            SELECT id, nome, data_criacao, estado, dados_json, valor_total 
            FROM orcamentos 
            WHERE usuario_id = ? 
            ORDER BY id DESC
        """, (usuario_id,))
    else:
        cursor.execute("""
            SELECT id, nome, data_criacao, estado, dados_json, valor_total 
            FROM orcamentos 
            WHERE usuario_id IS NULL
            ORDER BY id DESC
        """)
    rows = cursor.fetchall()
    conn.close()
    
    lista = []
    for r in rows:
        lista.append({
            "id": r[0],
            "nome": r[1],
            "data_criacao": r[2],
            "estado": r[3],
            "dados_json": json.loads(r[4]),
            "valor_total": r[5]
        })
    return lista

def atualizar_nome_orcamento(item_id: int, novo_nome: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("UPDATE orcamentos SET nome = ? WHERE id = ?", (novo_nome, item_id))
    conn.commit()
    conn.close()

def excluir_orcamento(item_id: int):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM orcamentos WHERE id = ?", (item_id,))
    conn.commit()
    conn.close()

def duplicar_orcamento(item_id: int, usuario_id: int, novo_nome: str) -> int:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT estado, dados_json, valor_total FROM orcamentos WHERE id = ?", (item_id,))
    r = cursor.fetchone()
    conn.close()
    
    if r:
        return salvar_orcamento(
            usuario_id=usuario_id,
            nome=novo_nome,
            estado=r[0],
            dados=json.loads(r[1]),
            valor_total=r[2]
        )
    return -1

def quantidade_orcamentos_salvos(usuario_id: int = None) -> int:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    if usuario_id is not None:
        cursor.execute("SELECT COUNT(*) FROM orcamentos WHERE usuario_id = ?", (usuario_id,))
    else:
        cursor.execute("SELECT COUNT(*) FROM orcamentos WHERE usuario_id IS NULL")
    total = cursor.fetchone()[0]
    conn.close()
    return total