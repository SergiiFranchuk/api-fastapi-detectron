import uvicorn
from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

import settings
from views import router as tasks_router
from users.views import router as users_router


application = FastAPI()
application.include_router(tasks_router)
application.include_router(users_router)


register_tortoise(application, config=settings.TORTOISE_ORM_CONFIG)
