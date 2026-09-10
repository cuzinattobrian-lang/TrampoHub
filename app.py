from flask import Flask, render_template, request, redirect, url_for, session, g
from werkzeug.security import generate_password_hash, check_password_hash
 
from database import SessionLocal, init_db
from models import Usuario, Vaga, Candidatura
 
app = Flask(__name__)
 
# CONFIGURAÇÃO
 
app.secret_key = "trampohub-chave-secreta-2026"
 
# Cria o arquivo trampohub.db e as tabelas, se ainda não existirem.
init_db()
 
def get_db():
    if "db" not in g:
        g.db = SessionLocal()
    return g.db
 
 
@app.teardown_appcontext
def close_db(exception=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()
 
 
# FUNÇÕES AUXILIARES
 
def usuario_logado():
    """Retorna o usuário atualmente conectado (ou None)."""
 
    usuario_id = session.get("usuario_id")
 
    if usuario_id is None:
        return None
 
    return get_db().get(Usuario, usuario_id)
 
 
def exigir_login():
    """Verifica se existe usuário logado. Retorna o usuário ou None."""
    return usuario_logado()
 
# PÁGINA INICIAL
 
@app.route("/")
def inicio():
 
    usuario = usuario_logado()
 
    if usuario:
 
        if usuario.tipo == "candidato":
            return redirect(url_for("candidato"))
 
        if usuario.tipo == "empresa":
            return redirect(url_for("empresa"))
 
    return render_template("index.html")
 
 
# CADASTRO
 
@app.route("/cadastro")
def cadastro():
    return render_template("cadastro.html")
 
# CADASTRO DE CANDIDATO
 
@app.route("/cadastro/candidato", methods=["GET", "POST"])
def cadastro_candidato():
 
    if request.method == "GET":
        return render_template("cadastro_candidato.html", erro=None)
 
    db = get_db()
 
    nome = request.form.get("nome", "").strip()
    email = request.form.get("email", "").strip().lower()
    telefone = request.form.get("telefone", "").strip()
    endereco = request.form.get("endereco", "").strip()
    experiencias = request.form.get("experiencias", "").strip()
    senha = request.form.get("senha", "")
    confirmar_senha = request.form.get("confirmar_senha", "")
 
    # VALIDAÇÕES
 
    if not nome or not email or not senha:
        return render_template(
            "cadastro_candidato.html",
            erro="Preencha todos os campos obrigatórios.",
        )
 
    if senha != confirmar_senha:
        return render_template(
            "cadastro_candidato.html",
            erro="As senhas não são iguais.",
        )
 
    # Verifica e-mail duplicado (agora é uma consulta SQL via SQLAlchemy)
 
    email_existente = db.query(Usuario).filter(Usuario.email == email).first()
 
    if email_existente:
        return render_template(
            "cadastro_candidato.html",
            erro="Este e-mail já está cadastrado.",
        )
 
    # CRIA USUÁRIO
 
    novo_usuario = Usuario(
        tipo="candidato",
        nome=nome,
        email=email,
        telefone=telefone,
        endereco=endereco,
        experiencias=experiencias,
        senha=generate_password_hash(senha),
    )
 
    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)
 
    # Login automático
 
    session["usuario_id"] = novo_usuario.id
 
    return redirect(url_for("candidato"))
 
# CADASTRO DE EMPRESA
 
@app.route("/cadastro/empresa", methods=["GET", "POST"])
def cadastro_empresa():
 
    if request.method == "GET":
        return render_template("cadastro_empresa.html", erro=None)
 
    db = get_db()
 
    nome = request.form.get("nome", "").strip()
    cnpj = request.form.get("cnpj", "").strip()
    email = request.form.get("email", "").strip().lower()
    telefone = request.form.get("telefone", "").strip()
    endereco = request.form.get("endereco", "").strip()
    area = request.form.get("area", "").strip()
    descricao = request.form.get("descricao", "").strip()
    senha = request.form.get("senha", "")
    confirmar_senha = request.form.get("confirmar_senha", "")
 
    # VALIDAÇÕES
 
    if not nome or not email or not senha:
        return render_template(
            "cadastro_empresa.html",
            erro="Preencha todos os campos obrigatórios.",
        )
 
    if senha != confirmar_senha:
        return render_template(
            "cadastro_empresa.html",
            erro="As senhas não são iguais.",
        )
 
    email_existente = db.query(Usuario).filter(Usuario.email == email).first()
 
    if email_existente:
        return render_template(
            "cadastro_empresa.html",
            erro="Este e-mail já está cadastrado.",
        )
 
    # CRIA EMPRESA
 
    nova_empresa = Usuario(
        tipo="empresa",
        nome=nome,
        cnpj=cnpj,
        email=email,
        telefone=telefone,
        endereco=endereco,
        area=area,
        descricao=descricao,
        senha=generate_password_hash(senha),
    )
 
    db.add(nova_empresa)
    db.commit()
    db.refresh(nova_empresa)
 
    session["usuario_id"] = nova_empresa.id
 
    return redirect(url_for("empresa"))
 
    # LOGIN
 
@app.route("/login", methods=["GET", "POST"])
def login():
 
    if request.method == "GET":
        tipo = request.args.get("tipo", "")
        return render_template("login.html", tipo=tipo, erro=None)
 
    db = get_db()
 
    tipo = request.form.get("tipo", "").strip()
    email = request.form.get("email", "").strip().lower()
    senha = request.form.get("senha", "")
 
    if not tipo:
        tipo = "candidato"
 
    if not email or not senha:
        return render_template(
            "login.html",
            tipo=tipo,
            erro="Preencha o e-mail e a senha.",
        )
 
    usuario_encontrado = (
        db.query(Usuario)
        .filter(Usuario.email == email)
        .first()
    )
 
    if usuario_encontrado is None:
        return render_template(
            "login.html",
            tipo=tipo,
            erro="E-mail ou senha incorretos.",
        )
 
    senha_correta = check_password_hash(usuario_encontrado.senha, senha)
 
    if not senha_correta:
        return render_template(
            "login.html",
            tipo=tipo,
            erro="E-mail ou senha incorretos.",
        )
 
    session["usuario_id"] = usuario_encontrado.id
 
    if usuario_encontrado.tipo == "candidato":
        return redirect(url_for("candidato"))
 
    return redirect(url_for("empresa"))
 
# LOGOUT
 
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("inicio"))
 
# PAINEL DO CANDIDATO
 
@app.route("/candidato")
def candidato():
 
    usuario = exigir_login()
 
    if not usuario:
        return redirect(url_for("login", tipo="candidato"))
 
    if usuario.tipo != "candidato":
        return redirect(url_for("empresa"))
 
    db = get_db()
 
    candidaturas = (
        db.query(Candidatura)
        .filter(Candidatura.candidato_id == usuario.id)
        .all()
    )
 
    total_candidaturas = len(candidaturas)
    em_analise = sum(1 for c in candidaturas if c.status == "Em Análise")
    aprovadas = sum(1 for c in candidaturas if c.status == "Aprovado")
 
    return render_template(
        "candidato.html",
        candidato=usuario,
        total_candidaturas=total_candidaturas,
        em_analise=em_analise,
        aprovadas=aprovadas,
    )
 
# MEU PERFIL (CANDIDATO)
 
@app.route("/candidato/perfil", methods=["GET", "POST"])
def meu_perfil():
 
    usuario = exigir_login()
 
    if not usuario:
        return redirect(url_for("login", tipo="candidato"))
 
    if usuario.tipo != "candidato":
        return redirect(url_for("empresa"))
 
    db = get_db()
 
    erro = None
    sucesso = None
 
    if request.method == "POST":
 
        nome = request.form.get("nome", "").strip()
        email = request.form.get("email", "").strip().lower()
        telefone = request.form.get("telefone", "").strip()
        endereco = request.form.get("endereco", "").strip()
        experiencias = request.form.get("experiencias", "").strip()
 
        if not nome or not email:
            erro = "Nome e e-mail são obrigatórios."
        else:
            email_em_uso = (
                db.query(Usuario)
                .filter(Usuario.email == email, Usuario.id != usuario.id)
                .first()
            )
 
            if email_em_uso:
                erro = "Este e-mail já está sendo usado."
            else:
                usuario.nome = nome
                usuario.email = email
                usuario.telefone = telefone
                usuario.endereco = endereco
                usuario.experiencias = experiencias
                db.commit()
                sucesso = "Perfil atualizado com sucesso!"
 
    return render_template(
        "meu_perfil.html",
        candidato=usuario,
        erro=erro,
        sucesso=sucesso,
    )
 
# VAGAS DISPONÍVEIS (CANDIDATO)
 
@app.route("/vagas")
def vagas():
 
    usuario = exigir_login()
 
    if not usuario:
        return redirect(url_for("login", tipo="candidato"))
 
    if usuario.tipo != "candidato":
        return redirect(url_for("empresa"))
 
    db = get_db()
 
    termo_busca = request.args.get("busca", "").strip()
 
    consulta = db.query(Vaga)
 
    if termo_busca:
        like = f"%{termo_busca}%"
        consulta = consulta.join(Usuario, Vaga.empresa_id == Usuario.id).filter(
            (Vaga.titulo.ilike(like))
            | (Vaga.descricao.ilike(like))
            | (Usuario.nome.ilike(like))
        )
 
    lista_vagas = consulta.all()
 
    return render_template(
        "vagas.html",
        vagas=lista_vagas,
        termo_busca=termo_busca,
        candidato=usuario,
    )
 
# DETALHES DE UMA VAGA
 
@app.route("/vagas/<int:id>")
def detalhes_vaga(id):
 
    usuario = exigir_login()
 
    if not usuario:
        return redirect(url_for("login", tipo="candidato"))
 
    if usuario.tipo != "candidato":
        return redirect(url_for("empresa"))
 
    db = get_db()
 
    vaga = db.get(Vaga, id)
 
    if not vaga:
        return redirect(url_for("vagas"))
 
    ja_candidatou = (
        db.query(Candidatura)
        .filter(
            Candidatura.candidato_id == usuario.id,
            Candidatura.vaga_id == vaga.id,
        )
        .first()
        is not None
    )
 
    return render_template(
        "detalhes_vaga.html",
        vaga=vaga,
        ja_candidatou=ja_candidatou,
    )
 
# CANDIDATAR-SE A UMA VAGA
 
@app.route("/vagas/<int:vaga_id>/candidatar", methods=["POST"])
def candidatar(vaga_id):
 
    usuario = exigir_login()
 
    if not usuario:
        return redirect(url_for("login", tipo="candidato"))
 
    if usuario.tipo != "candidato":
        return redirect(url_for("empresa"))
 
    db = get_db()
 
    vaga = db.get(Vaga, vaga_id)
 
    if vaga:
 
        ja_existe = (
            db.query(Candidatura)
            .filter(
                Candidatura.candidato_id == usuario.id,
                Candidatura.vaga_id == vaga.id,
            )
            .first()
        )
 
        if not ja_existe:
            nova_candidatura = Candidatura(
                candidato_id=usuario.id,
                vaga_id=vaga.id,
                status="Em Análise",
            )
            db.add(nova_candidatura)
            db.commit()
 
    return redirect(url_for("detalhes_vaga", id=vaga_id))
 
 
# MINHAS CANDIDATURAS (CANDIDATO)
 
@app.route("/candidato/candidaturas")
def minhas_candidaturas():
 
    usuario = exigir_login()
 
    if not usuario:
        return redirect(url_for("login", tipo="candidato"))
 
    if usuario.tipo != "candidato":
        return redirect(url_for("empresa"))
 
    db = get_db()
 
    candidaturas = (
        db.query(Candidatura)
        .filter(Candidatura.candidato_id == usuario.id)
        .all()
    )
 
    return render_template("minhas_candidaturas.html", candidaturas=candidaturas)
 
 
# PAINEL DA EMPRESA
 
@app.route("/empresa")
def empresa():
 
    usuario = exigir_login()
 
    if not usuario:
        return redirect(url_for("login", tipo="empresa"))
 
    if usuario.tipo != "empresa":
        return redirect(url_for("candidato"))
 
    db = get_db()
 
    vagas_empresa_lista = (
        db.query(Vaga).filter(Vaga.empresa_id == usuario.id).all()
    )
 
    vaga_ids = [v.id for v in vagas_empresa_lista]
 
    candidatos = (
        db.query(Candidatura).filter(Candidatura.vaga_id.in_(vaga_ids)).all()
        if vaga_ids
        else []
    )
 
    total_vagas = len(vagas_empresa_lista)
    total_candidatos = len(candidatos)
    em_analise = sum(1 for c in candidatos if c.status == "Em Análise")
 
    return render_template(
        "empresa.html",
        empresa=usuario,
        total_vagas=total_vagas,
        total_candidatos=total_candidatos,
        em_analise=em_analise,
    )
 
 
# PERFIL DA EMPRESA
 
 
@app.route("/empresa/perfil", methods=["GET", "POST"])
def empresa_perfil():
 
    usuario = exigir_login()
 
    if not usuario:
        return redirect(url_for("login", tipo="empresa"))
 
    if usuario.tipo != "empresa":
        return redirect(url_for("candidato"))
 
    db = get_db()
 
    mensagem = None
    erro = None
 
    if request.method == "POST":
 
        nome = request.form.get("nome", "").strip()
        cnpj = request.form.get("cnpj", "").strip()
        email = request.form.get("email", "").strip().lower()
        telefone = request.form.get("telefone", "").strip()
        endereco = request.form.get("endereco", "").strip()
        area = request.form.get("area", "").strip()
        descricao = request.form.get("descricao", "").strip()
 
        if not nome or not email:
            erro = "Nome e e-mail são obrigatórios."
        else:
            email_em_uso = (
                db.query(Usuario)
                .filter(Usuario.email == email, Usuario.id != usuario.id)
                .first()
            )
 
            if email_em_uso:
                erro = "Este e-mail já está sendo usado."
            else:
                usuario.nome = nome
                usuario.cnpj = cnpj
                usuario.email = email
                usuario.telefone = telefone
                usuario.endereco = endereco
                usuario.area = area
                usuario.descricao = descricao
                db.commit()
                mensagem = "Perfil atualizado com sucesso!"
 
    return render_template(
        "empresa_perfil.html",
        empresa=usuario,
        mensagem=mensagem,
        erro=erro,
    )
 
 
# CRIAR NOVA VAGA
 
@app.route("/empresa/nova-vaga", methods=["GET", "POST"])
def nova_vaga():
 
    usuario = exigir_login()
 
    if not usuario:
        return redirect(url_for("login", tipo="empresa"))
 
    if usuario.tipo != "empresa":
        return redirect(url_for("candidato"))
 
    if request.method == "GET":
        return render_template("nova_vaga.html", erro=None)
 
    db = get_db()
 
    titulo = request.form.get("titulo", "").strip()
    descricao = request.form.get("descricao", "").strip()
    requisitos = request.form.get("requisitos", "").strip()
    salario = request.form.get("salario", "").strip()
    modalidade = request.form.get("modalidade", "").strip()
    contrato = request.form.get("contrato", "").strip()
 
    if not titulo or not descricao or not requisitos or not modalidade or not contrato:
        return render_template(
            "nova_vaga.html",
            erro="Preencha todos os campos obrigatórios.",
        )
 
    nova_vaga_registro = Vaga(
        empresa_id=usuario.id,
        titulo=titulo,
        descricao=descricao,
        requisitos=requisitos,
        salario=salario,
        modalidade=modalidade,
        contrato=contrato,
    )
 
    db.add(nova_vaga_registro)
    db.commit()
 
    return redirect(url_for("vagas_empresa"))
 
 
# MINHAS VAGAS DA EMPRESA
 
@app.route("/empresa/vagas")
def vagas_empresa():
 
    usuario = exigir_login()
 
    if not usuario:
        return redirect(url_for("login", tipo="empresa"))
 
    if usuario.tipo != "empresa":
        return redirect(url_for("candidato"))
 
    db = get_db()
 
    minhas_vagas = db.query(Vaga).filter(Vaga.empresa_id == usuario.id).all()
 
    return render_template("vagas_empresa.html", vagas=minhas_vagas)
 
 
# CANDIDATOS DA EMPRESA
 
@app.route("/empresa/candidatos")
def candidatos_empresa():
 
    usuario = exigir_login()
 
    if not usuario:
        return redirect(url_for("login", tipo="empresa"))
 
    if usuario.tipo != "empresa":
        return redirect(url_for("candidato"))
 
    db = get_db()
 
    vaga_ids = [
        v.id for v in db.query(Vaga.id).filter(Vaga.empresa_id == usuario.id).all()
    ]
 
    candidaturas = (
        db.query(Candidatura).filter(Candidatura.vaga_id.in_(vaga_ids)).all()
        if vaga_ids
        else []
    )
 
    return render_template("candidatos.html", candidaturas=candidaturas)
 
 
# ALTERAR STATUS DA CANDIDATURA
 
@app.route("/empresa/mudar-status/<int:id>", methods=["POST"])
def empresa_mudar_status(id):
 
    usuario = exigir_login()
 
    if not usuario:
        return redirect(url_for("login", tipo="empresa"))
 
    if usuario.tipo != "empresa":
        return redirect(url_for("candidato"))
 
    db = get_db()
 
    candidatura = db.get(Candidatura, id)
 
    if candidatura and candidatura.vaga.empresa_id == usuario.id:
 
        ciclo_status = {
            "Em Análise": "Aprovado",
            "Aprovado": "Reprovado",
        }
 
        candidatura.status = ciclo_status.get(candidatura.status, "Em Análise")
        db.commit()
 
    return redirect(url_for("candidatos_empresa"))
 
 
# COMPATIBILIDADE COM O FORMULÁRIO ANTIGO
 
@app.route("/formulario")
def formulario():
 
    usuario = usuario_logado()
 
    if usuario:
 
        if usuario.tipo == "candidato":
            return redirect(url_for("vagas"))
 
        if usuario.tipo == "empresa":
            return redirect(url_for("empresa"))
 
    return redirect(url_for("login", tipo="candidato"))
 
# EXECUÇÃO
 
if __name__ == "__main__":
    app.run(debug=True)