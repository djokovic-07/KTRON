import sqlite3

def update_db():
    with sqlite3.connect("users.db") as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("ALTER TABLE users ADD COLUMN cpf TEXT")
            conn.commit()
            print("Banco de dados atualizado: CPF adicionado!")
        except sqlite3.OperationalError:
            print("A coluna CPF já existe no banco de dados.")

update_db()
