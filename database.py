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

# Classe base da qual todos os modelos (Usuario, Vaga, Candidatura)
Base = declarative_base()


def init_db():
    """Cria as tabelas no banco (se ainda não existirem)."""
    import models  # noqa: F401  (garante que os modelos sejam registrados)
    Base.metadata.create_all(bind=engine)