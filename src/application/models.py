from tortoise import Model, fields


class Task(Model):
    id = fields.UUIDField(pk=True)
    owner = fields.ForeignKeyField("users.User", related_name="tasks")
    started_at = fields.DatetimeField(auto_now_add=True)
    finished_at = fields.DatetimeField(null=True)
    worker_task_id = fields.UUIDField()
