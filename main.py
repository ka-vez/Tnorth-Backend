from fastapi import FastAPI


app = FastAPI()

@app.get("/")
async def healthy():
    return {"detail" : "Working Perfectly"}