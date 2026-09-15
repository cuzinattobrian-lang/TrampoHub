from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class Usuario(Base):

    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, autoincrement=True)
    tipo = Column(String(20), nullable=False)  # "candidato" ou "empresa"

    # Campos comuns aos dois tipos
    nome = Column(String(150), nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    telefone = Column(String(30))
    endereco = Column(String(200))
    senha = Column(String(255), nullable=False)

    # Só usado quando tipo == "candidato"
    experiencias = Column(Text)

    # Só usado quando tipo == "empresa"
    cnpj = Column(String(20))
    area = Column(String(100))
    descricao = Column(Text)

    vagas = relationship(
        "Vaga",
        back_populates="empresa",
        cascade="all, delete-orphan",
    )

    candidaturas = relationship(
        "Candidatura",
        back_populates="candidato",
        cascade="all, delete-orphan",
    )


class Vaga(Base):
    __tablename__ = "vagas"

    id = Column(Integer, primary_key=True, autoincrement=True)
    empresa_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)

    titulo = Column(String(150), nullable=False)
    descricao = Column(Text, nullable=False)
    requisitos = Column(Text)
    salario = Column(String(50))
    modalidade = Column(String(30), nullable=False)
    contrato = Column(String(30), nullable=False)

    empresa = relationship("Usuario", back_populates="vagas")

    candidaturas = relationship(
        "Candidatura",
        back_populates="vaga",
        cascade="all, delete-orphan",
    )

    @property
    def empresa_nome(self):
        """Mantém compatibilidade com os templates, que usam vaga.empresa_nome."""
        return self.empresa.nome if self.empresa else None


class Candidatura(Base):
    __tablename__ = "candidaturas"

    id = Column(Integer, primary_key=True, autoincrement=True)
    candidato_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    vaga_id = Column(Integer, ForeignKey("vagas.id"), nullable=False)
    status = Column(String(20), nullable=False, default="Em Análise")

    candidato = relationship("Usuario", back_populates="candidaturas")
    vaga = relationship("Vaga", back_populates="candidaturas")


    @property
    def candidato_nome(self):
        return self.candidato.nome if self.candidato else None

    @property
    def candidato_email(self):
        return self.candidato.email if self.candidato else None

    @property
    def vaga_titulo(self):
        return self.vaga.titulo if self.vaga else None

    @property
    def empresa_id(self):
        return self.vaga.empresa_id if self.vaga else None

    @property
    def empresa_nome(self):
        return self.vaga.empresa.nome if self.vaga and self.vaga.empresa else None

    @property
    def modalidade(self):
        return self.vaga.modalidade if self.vaga else None

    @property
    def contrato(self):
        return self.vaga.contrato if self.vaga else None
