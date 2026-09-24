from flask import Flask

from database import init_app
from routes import bp as routes_bp

# CONFIGURAÇÃO

app = Flask(__name__)
app.secret_key = "trampohub-chave-secreta-2026"

# Cria o arquivo trampohub.db e as tabelas (se ainda não existirem)
# e registra o fechamento da sessão ao fim de cada requisição.
init_app(app)

# Registra todas as rotas da aplicação (definidas em routes.py)
app.register_blueprint(routes_bp)

# EXECUÇÃO

if __name__ == "__main__":
    app.run(debug=True)
