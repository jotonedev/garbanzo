from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from .config import Config


app = FastAPI(title="Garbanzo", version="0.1.0")
config: Config | None = None

# Mount static files
app.mount("/static", StaticFiles(directory="www/static"), name="static")


@app.get("/")
async def index():
    try:
        return FileResponse("www/index.html", media_type="text/html")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api")
async def read_api():
    return {"message": "Hello, World!"}


@app.get("/api/health")
async def read_health():
    return {"status": "ok"}


@app.on_event("startup")
async def startup_event():
    global config

    config = Config.load_from_file("config/config.json"

