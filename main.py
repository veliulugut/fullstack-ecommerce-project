from fastapi import FastAPI,Request
import uvicorn

app = FastAPI()


@app.get("/")
def main(request:Request)-> dict:
    return{
        "Message":"Hello World",
    }
    

if __name__ == "__main__":
    uvicorn.run("main:app",host="0.0.0.0",port=8080,reload=True)