from fastapi import FastAPI, Request
import uvicorn
from api import user
from database.connection import Base, engine

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(user.router, prefix="/user")

@app.get("/")
def main(request: Request) -> dict:
    return {"Message": "Hello World"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)