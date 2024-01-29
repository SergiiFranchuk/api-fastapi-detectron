from interfaces import AbstractRepository


class TortoiseRepository(AbstractRepository):
    model_class = None

    async def list(self, **filters):
        return await self.model_class.filter(**filters)

    async def create(self, data):
        return await self.model_class.create(**data)

    async def update(self, reference, data):
        return await self.model_class.filter(id=reference).update(**data)

    async def retrieve(self, reference):
        return await self.model_class.get_or_none(id=reference)

    async def delete(self, reference):
        return await self.model_class.filter(id=reference).delete()
