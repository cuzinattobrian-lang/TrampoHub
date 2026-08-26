from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Banco de dados temporário em memória
candidaturas = []


@app.route("/")
def inicio():
    # Cálculo das métricas para os Cards
    total_candidaturas = len(candidaturas)
    em_analise = sum(1 for c in candidaturas if c["status"] == "Em Análise")
    aprovadas = sum(1 for c in candidaturas if c["status"] == "Aprovado")

    # Tratamento da busca por nome ou vaga/categoria
    termo_busca = request.args.get("busca", "").strip().lower()
    if termo_busca:
        lista_exibicao = [
            c
            for c in candidaturas
            if termo_busca in c["nome"].lower()
            or termo_busca in c["vaga"].lower()
            or termo_busca in c["modalidade"].lower()
        ]
    else:
        lista_exibicao = candidaturas

    return render_template(
        "index.html",
        total=total_candidaturas,
        em_analise=em_analise,
        aprovadas=aprovadas,
        candidaturas=lista_exibicao,
        termo_busca=termo_busca,
    )


@app.route("/formulario")
def formulario():
    return render_template("formulario.html", erro=None)


@app.route("/cadastrar", methods=["POST"])
def cadastrar():
    nome = request.form.get("nome", "").strip()
    email = request.form.get("email", "").strip()
    vaga = request.form.get("vaga", "").strip()
    modalidade = request.form.get("modalidade", "").strip()
    contrato = request.form.get("contrato", "").strip()

    # Validação de back-end: rejeita campos vazios
    if not nome or not email or not vaga or not modalidade or not contrato:
        return render_template(
            "formulario.html",
            erro="Preencha todos os campos obrigatórios!",
        )

    # Criação do novo registro com ID único e status padrão
    novo_id = len(candidaturas) + 1
    nova_candidatura = {
        "id": novo_id,
        "nome": nome,
        "email": email,
        "vaga": vaga,
        "modalidade": modalidade,
        "contrato": contrato,
        "status": "Em Análise",
    }

    candidaturas.append(nova_candidatura)
    return redirect(url_for("inicio"))


@app.route("/mudar-status/<int:id>", methods=["POST"])
def mudar_status(id):
    for c in candidaturas:
        if c["id"] == id:
            # Alterna o status entre 'Em Análise' e 'Aprovado'
            if c["status"] == "Em Análise":
                c["status"] = "Aprovado"
            else:
                c["status"] = "Em Análise"
            break
    return redirect(url_for("inicio"))


if __name__ == "__main__":
    app.run(debug=True)