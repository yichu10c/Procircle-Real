from typing import Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.selectable import Select as SelectBase, TableClause
from sqlalchemy.sql import Insert as InsertBase, Update as UpdateBase, Delete as DeleteBase

from app.tools.sql import Base


class Select(SelectBase):
    inherit_cache = True

    def __init__(self, *entities, session: Optional[AsyncSession]):
        super().__init__(*entities)
        self.session = session
        self.is_single_object = len(entities) == 1 and issubclass(entities[0], Base)

    async def get_scalar(self):
        result = await self.session.execute(self)
        scalar_result = result.scalars()
        return scalar_result

    async def all(self):
        res = await self.session.execute(self)
        res = res.all()
        if self.is_single_object and res:
            return [r[0] for r in res]
        return res

    async def first(self):
        res = await self.session.execute(self)
        res = res.first()
        if self.is_single_object and res:
            return list(res)[0]
        return res


class Insert(InsertBase):
    inherit_cache = True
    def __init__(self, table: TableClause, session: Optional[AsyncSession]):
        super().__init__(table)
        self.session = session

    async def insert_row(self) -> int:
        result = await self.session.execute(self)
        await self.session.commit()
        if not result.is_insert:
            return 0
        return result.inserted_primary_key[0]


class Update(UpdateBase):
    inherit_cache = True
    def __init__(self, table: TableClause, session: Optional[AsyncSession]):
        super().__init__(table)
        self.session = session

    async def update_row(self) -> int:
        try:
            await self.session.execute(self)
            await self.session.commit()
            return 1
        except Exception as e:
            return 0


class Delete(DeleteBase):
    inherit_cache = True
    def __init__(self, table: TableClause, session: Optional[AsyncSession]):
        super().__init__(table)
        self.session = session

    async def delete_row(self) -> int:
        try:
            await self.session.execute(self)
            await self.session.commit()
            return 1
        except:
            return 0


class SessionWrapper:
    def __init__(self, session):
        self.session = session

    def select(self, *entities):
        return Select(*entities, session=self.session)

    def insert(self, table: TableClause):
        return Insert(table, session=self.session)

    def update(self, table: TableClause):
        return Update(table, session=self.session)

    def delete(self, table: TableClause):
        return Delete(table, session=self.session)


def within(session: AsyncSession):
    return SessionWrapper(session)


# utils
def as_dict(entity):
    if not entity:
        return entity
    if isinstance(entity, Base):
        return {
            k: v for k, v in vars(entity).items()
            if not k.startswith("__")
            and not k.endswith("__")
            and k != "_sa_instance_state"
        }
    if isinstance(entity, (list, tuple)):
        return [as_dict(ent) for ent in entity]
    return entity._asdict()
