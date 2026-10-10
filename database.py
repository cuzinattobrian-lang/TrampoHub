import os

from flask import g
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Arquivo único onde o SQLite vai guardar tudo
DATABASE_URL = "sqlite:///trampohub.db"

# Pasta onde as imagens enviadas pelos usuários (upload) são salvas
UPLOAD_FOLDER = os.path.join("static", "uploads")


engine = create_engine(
    DATABASE_URL,
    echo=True,
    connect_args={"check_same_thread": False},
)

# Fábrica de sessões
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

# Classe base da qual todos os modelos (Usuario, Vaga, Candidatura) herdam
Base = declarative_base()


def init_db():
    """Cria as tabelas no banco (se ainda não existirem) e garante que a
    pasta de uploads e as colunas novas existam."""
    import models  # noqa: F401  (garante que os modelos sejam registrados)
    Base.metadata.create_all(bind=engine)
    _migrar_colunas_novas()
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def _migrar_colunas_novas():
    """Base.metadata.create_all só cria tabelas que ainda não existem — ele
    não adiciona colunas novas em tabelas já criadas anteriormente. Como o
    SQLite não migra sozinho, adicionamos aqui a coluna "imagem" em bancos
    (trampohub.db) que já existiam antes dela ser criada no model Vaga.
    """
    with engine.connect() as conn:
        colunas = [linha[1] for linha in conn.exec_driver_sql("PRAGMA table_info(vagas)")]
        if "imagem" not in colunas:
            conn.exec_driver_sql(
                "ALTER TABLE vagas ADD COLUMN imagem VARCHAR(255) DEFAULT 'padrao.png'"
            )
            conn.commit()


def get_db():
    """Retorna a sessão do banco ligada ao contexto da requisição atual.

    Usa flask.g para garantir uma única sessão por requisição, reaproveitada
    por todas as rotas que precisarem dela.
    """
    if "db" not in g:
        g.db = SessionLocal()
    return g.db


def close_db(exception=None):
    """Fecha a sessão do banco ao final de cada requisição."""
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_app(app):
    """Prepara o banco e registra os hooks de sessão na aplicação Flask."""
    init_db()
    app.teardown_appcontext(close_db)
