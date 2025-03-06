from flask import Flask, render_template, request, redirect, flash, session, url_for
import sqlite3
import re

app = Flask(__name__)
app.secret_key = "secreta"


def init_db():
    with sqlite3.connect("users.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            is_admin INTEGER NOT NULL DEFAULT 0,
            cpf TEXT
        )
        """)
    print("Banco de dados inicializado!")


@app.route("/")
def home():
    return render_template("home.html")

@app.route("/login")
def login_page():
    return render_template("login.html")

@app.route("/register")
def register_page():
    return render_template("register.html")

@app.route("/pagamento")
def pagamento_page():
    return render_template("pagamento.html")


@app.route("/pagamentocartao")
def payment_form():
    return render_template('pagamentocartao.html')

@app.route("/register.html")
def register_form():
    return render_template('register.html')

@app.route("/pagamentopix")
def pix_form():
    return render_template('pagamentopix.html')


@app.route("/agradecimentocompra", methods=["POST", "GET"])
def agradecimentocompra():
    if request.method == "POST":
        nome_comprador = request.form['name']  # Nome vindo do formulário
    else:
        # Nome vindo da URL, se aplicável
        nome_comprador = request.args.get('nome')

    return render_template('agradecimentocompra.html', nome=nome_comprador)


@app.route("/register", methods=["POST"])
def register():
    username = request.form.get("username")
    password = request.form.get("password")
    is_admin = 1 if request.form.get("is_admin") else 0  
    cpf = request.form.get("cpf") if is_admin else None  

    if not username or not password:
        flash("Preencha todos os campos!", "error")
        return redirect("/register")

    # Validação do CPF (se o usuário for admin)
    if is_admin and (not cpf or not re.match(r"^\d{11}$", cpf)):
        flash("CPF inválido! Insira 11 números.", "error")
        return redirect("/register")

    try:
        with sqlite3.connect("users.db") as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO users (username, password, is_admin, cpf) VALUES (?, ?, ?, ?)", 
                (username, password, is_admin, cpf)
            )
            conn.commit()
        flash("Registro realizado com sucesso!", "success")
    except sqlite3.IntegrityError:
        flash("Usuário já existe.", "error")
    return redirect("/register")


@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")
    is_admin = request.form.get("is_admin") 
    cpf = request.form.get("cpf") if is_admin else None 

    if not username or not password:
        flash("Preencha todos os campos!", "error")
        return redirect("/login")

    with sqlite3.connect("users.db") as conn:
        cursor = conn.cursor()

        if not is_admin:
            cursor.execute(
                "SELECT id, username, is_admin FROM users WHERE username = ? AND password = ?",
                (username, password)
            )
        else:
            if not cpf or not re.match(r"^\d{11}$", cpf):
                flash("CPF inválido! Insira 11 números.", "error")
                return redirect("/login")

            cursor.execute(
                "SELECT id, username, is_admin FROM users WHERE username = ? AND password = ? AND cpf = ? AND is_admin = 1",
                (username, password, cpf)
            )

        user = cursor.fetchone()

        if user:
            session["user"] = user[1]
            session["is_admin"] = user[2]
            flash("Login realizado com sucesso!", "success")
            return redirect("/catalog" if user[2] else "/catalog")
        else:
            flash("Credenciais inválidas.", "error")

    return redirect("/login")


@app.route("/catalog")
def dashboard():
    if "user" not in session:
        flash("Faça login primeiro!", "error")
        return redirect("/")
    return render_template("catalog.html", username=session["user"])

# Rota para logout


@app.route("/logout")
def logout():
    session.pop("user", None)
    flash("Logout realizado com sucesso.", "success")
    return redirect("/")


@app.route("/pagamento", methods=["GET", "POST"])
def forma_pagamento():
    if request.method == "POST":
        pagamento = request.form.get("pagamento")
        return render_template("confirmacao.html", pagamento=pagamento)
    return render_template("pagamento.html")


@app.route("/pagamentocartao", methods=['GET', 'POST'])
def pagamentocartao():
    name = request.form['name']

    return redirect(url_for('agradecimentocompra', nome=name))


@app.route('/pagamentopix', methods=['POST'])
def pagamentopix():
    name = request.form['name']

    return redirect(url_for('agradecimentocompra', nome=name))


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
