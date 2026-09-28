import os
from functools import lru_cache
from typing import Generator

from dotenv import load_dotenv
from sqlalchemy import DateTime, Integer, String, create_engine, func, select, text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, sessionmaker
from sqlalchemy.types import JSON

load_dotenv()

DEFAULT_DATABASE_URL = "postgresql+psycopg2://postgres:postgres@localhost:5432/agrosense_ai"


class Base(DeclarativeBase):
    pass


# JSONB is used on PostgreSQL. Generic JSON keeps the model testable on SQLite.
JsonType = JSON().with_variant(JSONB, "postgresql")


class Prediction(Base):
    __tablename__ = "predictions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    model_type: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    input_data: Mapped[dict] = mapped_column(JsonType, nullable=False)
    output_data: Mapped[dict] = mapped_column(JsonType, nullable=False)
    created_at: Mapped[object] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now(), index=True
    )


def _database_url() -> str:
    return os.getenv("DATABASE_URL", DEFAULT_DATABASE_URL)


@lru_cache(maxsize=1)
def get_engine():
    return create_engine(_database_url(), pool_pre_ping=True)


@lru_cache(maxsize=1)
def get_session_factory():
    return sessionmaker(bind=get_engine(), autoflush=False, autocommit=False, expire_on_commit=False)


def init_db() -> None:
    Base.metadata.create_all(bind=get_engine())


def get_db() -> Generator[Session, None, None]:
    db = get_session_factory()()
    try:
        yield db
    finally:
        db.close()


def database_status() -> bool:
    try:
        with get_engine().connect() as connection:
            connection.execute(text("SELECT 1"))
        return True
    except Exception:
        return False


def save_prediction(db: Session, model_type: str, input_data: dict, output_data: dict) -> Prediction:
    row = Prediction(
        model_type=model_type,
        input_data=input_data,
        output_data=output_data,
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


def fetch_predictions(db: Session, limit: int = 20, model_type: str | None = None) -> list[Prediction]:
    query = select(Prediction).order_by(Prediction.created_at.desc(), Prediction.id.desc())
    if model_type:
        query = query.where(Prediction.model_type == model_type)
    return list(db.scalars(query.limit(limit)).all())


def count_predictions(db: Session, model_type: str | None = None) -> int:
    query = select(func.count(Prediction.id))
    if model_type:
        query = query.where(Prediction.model_type == model_type)
    return int(db.scalar(query) or 0)
