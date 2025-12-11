import os
import datetime
from datetime import timedelta
import json
import csv
import sqlite3
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import base64
from flask import Flask, render_template, request, jsonify, session, redirect, url_for, Response
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'skyalp_chave_segura_final_v2'

# Configuração do Banco
basedir = os.path.abspath(os.path.dirname(__file__))
database_path = os.path.join(basedir, 'skyalp_production.db')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or f'sqlite:///{database_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAX_CONTENT_LENGTH'] = 32 * 1024 * 1024

db = SQLAlchemy(app)

@app.context_processor
def inject_globals():
    obra_atual = None
    if 'obra_id' in session:
        obra_atual = Obra.query.get(session['obra_id'])
    return dict(obra=obra_atual)

# === FUNÇÃO AUXILIAR DE FUSO HORÁRIO ===
def hora_brasil():
    return datetime.datetime.utcnow() - timedelta(hours=3)

# === MODELOS ===
obra_funcionarios = db.Table('obra_funcionarios',
    db.Column('funcionario_id', db.Integer, db.ForeignKey('funcionario.id'), primary_key=True),
    db.Column('obra_id', db.Integer, db.ForeignKey('obra.id'), primary_key=True)
)

class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    cnpj = db.Column(db.String(20))
    cidade = db.Column(db.String(50))
    obras = db.relationship('Obra', backref='cliente', lazy=True)

class Obra(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'), nullable=False)
    nome = db.Column(db.String(100), nullable=False)
    localizacao = db.Column(db.String(200))
    descricao = db.Column(db.Text)
    status = db.Column(db.String(50), default="Em Andamento")
    cor_primaria = db.Column(db.String(20), default="#0f766e")
    equipe = db.relationship('Funcionario', secondary=obra_funcionarios, lazy='subquery', backref=db.backref('obras_atribuidas', lazy=True))
    etapas = db.relationship('Etapa', backref='obra', lazy=True)
    registros = db.relationship('RegistroDiario', backref='obra', lazy=True)

class Funcionario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    funcao = db.Column(db.String(100))
    cpf = db.Column(db.String(20))
    telefone = db.Column(db.String(20))
    login = db.Column(db.String(50), unique=True)
    senha = db.Column(db.String(50))
    tipo_acesso = db.Column(db.String(20))

class Etapa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    obra_id = db.Column(db.Integer, db.ForeignKey('obra.id'), nullable=False)
    titulo = db.Column(db.String(100))
    prioridade = db.Column(db.String(20))
    data_inicio_prevista = db.Column(db.String(20))
    data_fim_prevista = db.Column(db.String(20))
    status = db.Column(db.String(50), default="Pendente")

class RegistroDiario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    obra_id = db.Column(db.Integer, db.ForeignKey('obra.id'), nullable=False)
    data_hora = db.Column(db.String(30))
    data_iso = db.Column(db.String(10))
    etapa_nome = db.Column(db.String(100))
    descricao = db.Column(db.Text)
    status_novo = db.Column(db.String(50))
    autor_nome = db.Column(db.String(100))
    foto = db.Column(db.Text)
    def to_dict(self):
        return {"id": self.id, "data": self.data_hora, "etapa": self.etapa_nome, "descricao": self.descricao, "status": self.status_novo, "autor": self.autor_nome, "foto": self.foto}

class Mensagem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    email = db.Column(db.String(100))
    telefone = db.Column(db.String(20))
    assunto = db.Column(db.String(100))
    mensagem = db.Column(db.Text)
    data_envio = db.Column(db.String(20))

def seed():
    with app.app_context():
        db.create_all()
        if not Funcionario.query.filter_by(login='admin').first():
            admin = Funcionario(nome="Admin Global", funcao="Diretor", login="admin", senha="admin", tipo_acesso="admin")
            db.session.add(admin)
            db.session.commit()

# --- ROTAS ---
@app.route('/')
def landing(): return render_template('landing.html')

@app.route('/login')
def login_page():
    if 'user_id' in session:
        u = Funcionario.query.get(session['user_id'])
        if u and u.tipo_acesso == 'admin': return redirect(url_for('portal_admin'))
        if u: return redirect(url_for('dashboard_operador'))
    return render_template('login.html')

@app.route('/portal')
def portal_admin():
    if 'user_id' not in session: return redirect(url_for('login_page'))
    u = Funcionario.query.get(session['user_id'])
    if not u or u.tipo_acesso != 'admin': return redirect(url_for('dashboard_operador'))
    return render_template('portal.html', usuario=u, clientes=Cliente.query.all(), mensagens=Mensagem.query.order_by(Mensagem.id.desc()).all(), funcionarios=Funcionario.query.all())

@app.route('/gerenciar_obra/<int:obra_id>')
def gerenciar_obra(obra_id):
    if 'user_id' not in session: return redirect(url_for('login_page'))
    u = Funcionario.query.get(session['user_id'])
    if not u or u.tipo_acesso != 'admin': return "Acesso Negado."
    session['obra_id'] = obra_id
    return redirect(url_for('page_gerente'))

@app.route('/gerente')
def page_gerente():
    if 'obra_id' not in session: return redirect(url_for('portal_admin'))
    oid = session['obra_id']
    todos_funcionarios = Funcionario.query.filter_by(tipo_acesso='operador').all()
    obra = Obra.query.get(oid)
    if not obra: return redirect(url_for('portal_admin'))

    # ATUALIZAÇÃO: Carrega todos os registros (chats) desta obra para o gerente ver
    registros = RegistroDiario.query.filter_by(obra_id=oid).order_by(RegistroDiario.id.desc()).all()

    return render_template('gerente.html',
                         equipe_atual=obra.equipe,
                         todos_funcionarios=todos_funcionarios,
                         etapas=Etapa.query.filter_by(obra_id=oid).all(),
                         registros=registros) # Passa os registros para o template

@app.route('/operador')
def dashboard_operador():
    if 'user_id' not in session: return redirect(url_for('login_page'))
    u = Funcionario.query.get(session['user_id'])
    if not u: return redirect(url_for('login_page'))
    if u.tipo_acesso == 'admin': return redirect(url_for('portal_admin'))
    return render_template('operador_menu.html', usuario=u, obras=u.obras_atribuidas)

@app.route('/operador/obra/<int:obra_id>')
def acessar_obra_operador(obra_id):
    if 'user_id' not in session: return redirect(url_for('login_page'))
    u = Funcionario.query.get(session['user_id'])
    obra = Obra.query.get(obra_id)
    if not obra or u not in obra.equipe: return "Você não tem acesso a esta obra."
    session['obra_id'] = obra_id
    registros = RegistroDiario.query.filter_by(obra_id=obra.id, autor_nome=u.nome).order_by(RegistroDiario.id.desc()).limit(20).all()
    etapas = Etapa.query.filter_by(obra_id=obra.id).all()
    return render_template('operador.html', usuario=u, obra=obra, etapas=etapas, registros=registros)

@app.route('/logout')
def logout(): session.clear(); return redirect(url_for('landing'))

# --- APIS ---
@app.route('/api/login_global', methods=['POST'])
def api_login_global():
    d = request.json; user = Funcionario.query.filter_by(login=d['user'], senha=d['pass']).first()
    if user: session['user_id'] = user.id; return jsonify({"status": "sucesso", "tipo": user.tipo_acesso})
    return jsonify({"status": "erro", "msg": "Credenciais inválidas"})

@app.route('/api/criar_cliente', methods=['POST'])
def api_criar_cliente(): d = request.json; db.session.add(Cliente(nome=d['nome'], cnpj=d.get('cnpj'), cidade=d.get('cidade'))); db.session.commit(); return jsonify({"msg": "OK"})

@app.route('/api/editar_cliente', methods=['POST'])
def api_editar_cliente():
    d = request.json; c = Cliente.query.get(d['id'])
    if c: c.nome = d['nome']; c.cnpj = d['cnpj']; c.cidade = d['cidade']; db.session.commit()
    return jsonify({"msg": "OK"})

@app.route('/api/criar_obra', methods=['POST'])
def api_criar_obra():
    d = request.json; nova = Obra(cliente_id=d['cliente_id'], nome=d['nome'], localizacao=d['local'], cor_primaria="#1e40af"); db.session.add(nova); db.session.commit()
    u = Funcionario.query.get(session['user_id'])
    if u and u not in nova.equipe: nova.equipe.append(u); db.session.commit()
    return jsonify({"msg": "OK", "id": nova.id})

@app.route('/api/editar_obra', methods=['POST'])
def api_editar_obra():
    d = request.json; o = Obra.query.get(d['id'])
    if o: o.nome = d['nome']; o.localizacao = d['local']; db.session.commit()
    return jsonify({"msg": "OK"})

@app.route('/api/criar_funcionario_global', methods=['POST'])
def criar_funcionario_global():
    d = request.json
    if Funcionario.query.filter_by(login=d['login']).first(): return jsonify({"msg": "Login já existe!"}), 400
    novo = Funcionario(nome=d['nome'], funcao=d['funcao'], cpf=d.get('cpf'), telefone=d.get('telefone'), login=d['login'], senha=d['senha'], tipo_acesso=d.get('tipo', 'operador'))
    db.session.add(novo); db.session.commit()
    return jsonify({"msg":"OK", "id": novo.id, "nome": novo.nome})

@app.route('/api/editar_funcionario', methods=['POST'])
def editar_funcionario():
    d = request.json; f = Funcionario.query.get(d['id'])
    if f:
        f.nome = d['nome']; f.funcao = d['funcao']; f.cpf = d['cpf']; f.telefone = d['telefone']; f.tipo_acesso = d['tipo']
        if f.login != d['login']:
            if Funcionario.query.filter_by(login=d['login']).first(): return jsonify({"msg": "Login já existe!"}), 400
            f.login = d['login']
        if d.get('senha'): f.senha = d['senha']
        db.session.commit()
    return jsonify({"msg": "OK"})

@app.route('/api/excluir_func', methods=['POST'])
def excluir_func(): d = request.json; f = Funcionario.query.get(d['id']); db.session.delete(f) if f else None; db.session.commit(); return jsonify({"msg": "OK"})

@app.route('/api/atribuir_funcionario', methods=['POST'])
def atribuir_funcionario():
    d = request.json; obra = Obra.query.get(session.get('obra_id')); func = Funcionario.query.get(d.get('funcionario_id'))
    if func and obra and func not in obra.equipe: obra.equipe.append(func); db.session.commit()
    return jsonify({"msg": "OK"})

@app.route('/api/remover_da_equipe', methods=['POST'])
def remover_da_equipe():
    d = request.json; obra = Obra.query.get(session.get('obra_id')); func = Funcionario.query.get(d.get('funcionario_id'))
    if func and obra and func in obra.equipe: obra.equipe.remove(func); db.session.commit()
    return jsonify({"msg": "OK"})

@app.route('/api/add_etapa', methods=['POST'])
def add_etapa(): d = request.json; db.session.add(Etapa(obra_id=session['obra_id'], titulo=d['titulo'], prioridade=d.get('prioridade'), data_inicio_prevista=d.get('inicio'), data_fim_prevista=d.get('fim'))); db.session.commit(); return jsonify({"msg":"OK"})

@app.route('/api/registrar', methods=['POST'])
def api_registrar():
    d=request.json; oid=session.get('obra_id'); uid=session.get('user_id'); func=Funcionario.query.get(uid);
    agora = hora_brasil()
    novo=RegistroDiario(obra_id=oid, data_hora=agora.strftime("%d/%m %H:%M"), data_iso=agora.strftime("%Y-%m-%d"), etapa_nome=d.get('etapa'), descricao=d.get('descricao'), status_novo=d.get('status'), foto=d.get('foto'), autor_nome=func.nome)
    etapa=Etapa.query.filter_by(obra_id=oid, titulo=d.get('etapa')).first()
    if etapa: etapa.status=d.get('status')
    db.session.add(novo); db.session.commit()
    return jsonify({"msg": "OK"})

@app.route('/api/enviar_contato', methods=['POST'])
def enviar_contato():
    d = request.json; agora = hora_brasil()
    db.session.add(Mensagem(nome=d.get('nome'), email=d.get('email'), telefone=d.get('telefone'), assunto=d.get('assunto'), mensagem=d.get('mensagem'), data_envio=agora.strftime("%d/%m/%Y %H:%M"))); db.session.commit(); return jsonify({"status": "sucesso"})

@app.route('/api/dashboard_analytics')
def dashboard_analytics():
    oid = session.get('obra_id')
    if not oid: return jsonify({"erro": "Sem obra"})
    etapas = Etapa.query.filter_by(obra_id=oid).all()
    fig = plt.figure(figsize=(10, 5)); ax = fig.add_subplot(111); sc = {};
    for e in etapas: sc[e.status] = sc.get(e.status, 0) + 1
    if sc: ax.pie(sc.values(), labels=sc.keys(), autopct='%1.0f%%')
    else: ax.text(0.5, 0.5, 'Sem dados', ha='center'); ax.axis('off')
    img = io.BytesIO(); plt.savefig(img, format='png'); img.seek(0)
    return jsonify({"imagem": f"data:image/png;base64,{base64.b64encode(img.getvalue()).decode()}"})

@app.route('/api/reset_sistema', methods=['POST'])
def reset(): db.drop_all(); seed(); return jsonify({"msg":"Resetado"})

@app.route('/exportar/csv')
def csv_exp(): return "CSV Download"
@app.route('/exportar/json')
def json_exp(): return jsonify([])
@app.route('/exportar/sql')
def sql_exp(): return "SQL Dump"

if __name__ == '__main__':
    seed()
    app.run(debug=True)