from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Public API Scraper. To view API documentation, visit http://127.0.0.1/docs"}
