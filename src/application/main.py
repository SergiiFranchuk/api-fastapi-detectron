from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise


from application import settings
from application.exception_handlers import (
    open_video_file_exception_handler,
    read_video_file_exception_handler,
)
from application.exceptions import CannotOpenVideoFileError, CannotReadVideoFileError
from application.users.exception_handlers import (
    password_mismatch_exception_handler,
)
from application.users.exceptions import MismatchPasswordError
from application.views import router as tasks_router
from application.users.views import router as users_router


application = FastAPI()


application.include_router(tasks_router)
application.include_router(users_router)
application.add_exception_handler(
    CannotOpenVideoFileError, open_video_file_exception_handler
)
application.add_exception_handler(
    CannotReadVideoFileError, read_video_file_exception_handler
)
application.add_exception_handler(
    MismatchPasswordError, password_mismatch_exception_handler
)


register_tortoise(application, config=settings.TORTOISE_ORM_CONFIG)
