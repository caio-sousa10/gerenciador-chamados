from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import datetime

app = Flask(__name__)

# Conectar ao banco de dados SQLite
def conectar_banco():
    conn = sqlite3.connect('chamados.db')
    return conn

# Criar a tabela de chamados, caso ela não exista
def criar_tabela():
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS chamados (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo TEXT NOT NULL,
            data DATETIME NOT NULL,
            observacao TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'pendente'
        )
    ''')
    conn.commit()
    conn.close()

# Rota principal (exibe o formulário de cadastro)
@app.route('/')
def index():
    return render_template('index.html')

# Rota para cadastrar um novo chamado
@app.route('/cadastrar', methods=['POST'])
def cadastrar_chamado():
    tipo = request.form['tipo']
    observacao = request.form['observacao']
    data = datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')

    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO chamados (tipo, data, observacao, status)
        VALUES (?, ?, ?, ?)
    ''', (tipo, data, observacao, 'pendente'))
    conn.commit()
    conn.close()

    return redirect(url_for('listar_chamados'))

# Rota para listar os chamados cadastrados (pendentes e feitos)
@app.route('/chamados')
def listar_chamados():
    conn = conectar_banco()
    cursor = conn.cursor()

    # Seleciona chamados pendentes e feitos
    cursor.execute("SELECT * FROM chamados WHERE status = 'pendente'")
    chamados_pendentes = cursor.fetchall()

    cursor.execute("SELECT * FROM chamados WHERE status = 'feito'")
    chamados_feitos = cursor.fetchall()

    conn.close()

    return render_template('index.html', chamados_pendentes=chamados_pendentes, chamados_feitos=chamados_feitos)

# Rota para marcar um chamado como 'feito'
@app.route('/marcar_como_feito/<int:chamado_id>', methods=['GET'])
def marcar_como_feito(chamado_id):
    conn = conectar_banco()
    cursor = conn.cursor()

    # Atualiza o status do chamado para 'feito'
    cursor.execute('UPDATE chamados SET status = "feito" WHERE id = ?', (chamado_id,))
    conn.commit()
    conn.close()

    return redirect(url_for('listar_chamados'))

# Rota para excluir um chamado
@app.route('/excluir_chamado/<int:chamado_id>', methods=['GET'])
def excluir_chamado(chamado_id):
    conn = conectar_banco()
    cursor = conn.cursor()

    # Deleta o chamado do banco de dados
    cursor.execute('DELETE FROM chamados WHERE id = ?', (chamado_id,))
    conn.commit()
    conn.close()

    return redirect(url_for('listar_chamados'))

if __name__ == '__main__':
    criar_tabela()  # Cria a tabela ao iniciar o app
    app.run(debug=True)
