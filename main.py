import uvicorn
from fastapi import FastAPI
from api import router as tasks_router


application = FastAPI()
application.include_router(tasks_router)


# @application.post("/signup/")
# async def sign_up(user: UserIn):
#     use_case = SignUpUseCase()
#     try:
#         return await use_case(user.model_dump())
#     except EmailError as error:
#         return JSONResponse(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             content={"email": error.args},
#         )


if __name__ == "__main__":
    uvicorn.run(
        "main:application", host="0.0.0.0", port=8000, log_level="info", reload=True
    )
