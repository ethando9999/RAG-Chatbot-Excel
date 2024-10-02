from fastapi import FastAPI
from app import router


app = FastAPI()

# Đăng ký router từ routes.py
app.include_router(router)


@app.get("/")
async def root():
    return {"message": "Success!"}