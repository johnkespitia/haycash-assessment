
from typing import Any, TypeVar

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.infrastructure.persistence.database import Base

ModelT = TypeVar("ModelT", bound=Base)


class BaseRepository[ModelT: Base]:
    def __init__(self, session: Session, model: type[ModelT]) -> None:
        self._session = session
        self._model = model

    def get_by_id(self, entity_id: Any) -> ModelT | None:
        return self._session.get(self._model, entity_id)

    def list_all(self) -> list[ModelT]:
        statement = select(self._model)
        return list(self._session.scalars(statement).all())

    def add(self, entity: ModelT) -> ModelT:
        self._session.add(entity)
        self._session.flush()
        return entity

    def update(self, entity: ModelT) -> ModelT:
        self._session.add(entity)
        self._session.flush()
        return entity

    def delete(self, entity: ModelT) -> None:
        self._session.delete(entity)
        self._session.flush()
