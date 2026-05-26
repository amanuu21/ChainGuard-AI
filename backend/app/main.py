from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database.connection import engine
from app.api.upload import router
from sqlalchemy import text

app = FastAPI()

# Add CORS middleware to allow frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://chain-guard-ai-sigma.vercel.app",
        "https://chain-guard-ai-git-main-amanuel-s-projects4.vercel.app",
        "https://*.vercel.app"  # Allows all Vercel preview deployments
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the upload router
app.include_router(router)

@app.get("/")
def home():
    return {"message": "ChainGuard AI Backend Running"}

@app.get("/test-db")
def test_database():
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            return {"database": "Connected Successfully", "result": result.scalar()}
    except Exception as e:
        return {"database": "Connection Failed", "error": str(e)}