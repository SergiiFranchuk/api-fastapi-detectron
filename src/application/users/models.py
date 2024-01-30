from tortoise import Model, fields


class BaseModel(Model):
    id = fields.IntField(pk=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        abstract = True


class User(BaseModel):
    email = fields.CharField(max_length=255, unique=True)
    first_name = fields.CharField(max_length=70)
    last_name = fields.CharField(max_length=70)
    password = fields.CharField(max_length=255)

    class Meta:
        table = "users"

    def __str__(self):
        return self.email
