from . import app


@app.get("/")
async def root():
    return "Hello world"


@app.get("/ping")
async def ping():
    return {"message": "pong"}
