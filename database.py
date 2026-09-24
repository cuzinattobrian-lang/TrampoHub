from flask import g
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Arquivo único onde o SQLite vai guardar tudo
DATABASE_URL = "sqlite:///trampohub.db"


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
    """Cria as tabelas no banco (se ainda não existirem)."""
    import models  # noqa: F401  (garante que os modelos sejam registrados)
    Base.metadata.create_all(bind=engine)


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
