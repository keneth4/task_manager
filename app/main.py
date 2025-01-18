from fastapi import FastAPI

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    print("Application running at: http://localhost:8000")


def hello():
    print("Hello world")


@app.get("/")
async def root()
    return "Hello world"
