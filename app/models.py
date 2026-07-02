import enum
from datetime import date
from typing import List

from sqlalchemy import ForeignKey, String, Integer, Date, Enum
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    """Classe base para todos os modelos do SQLAlchemy."""
    pass


class StatusFerias(enum.Enum):
    """Enumeração para garantir padronização nos status das férias."""
    PENDENTE = "Pendente"
    APROVADA = "Aprovada"
    RECUSADA = "Recusada"
    CONCLUIDA = "Concluída"


class Funcionario(Base):
    __tablename__ = "funcionarios"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(100), nullable=False)
    cargo: Mapped[str] = mapped_column(String(100), nullable=False)
    data_contratacao: Mapped[date] = mapped_column(Date, nullable=False)
    saldo_dias_ferias: Mapped[int] = mapped_column(Integer, default=30)

    # Relacionamento 1:N com EscalaFerias
    escalas: Mapped[List["EscalaFerias"]] = relationship(
        back_populates="funcionario", 
        cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Funcionario(nome='{self.nome}', cargo='{self.cargo}')>"


class EscalaFerias(Base):
    __tablename__ = "escala_ferias"

    id: Mapped[int] = mapped_column(primary_key=True)
    funcionario_id: Mapped[int] = mapped_column(ForeignKey("funcionarios.id"), nullable=False)
    data_inicio: Mapped[date] = mapped_column(Date, nullable=False)
    data_fim: Mapped[date] = mapped_column(Date, nullable=False)
    status: Mapped[StatusFerias] = mapped_column(
        Enum(StatusFerias), 
        default=StatusFerias.PENDENTE, 
        nullable=False
    )

    # Relacionamento de volta para Funcionario
    funcionario: Mapped["Funcionario"] = relationship(back_populates="escalas")

    def __repr__(self) -> str:
        return f"<EscalaFerias(inicio='{self.data_inicio}', fim='{self.data_fim}', status='{self.status.value}')>"