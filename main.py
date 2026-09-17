from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from VITO.api.routes import router

app = FastAPI(title="VITO — Veridian IT Orchestrator")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(router)


@app.get("/")
def root():
    return {"status": "ok", "service": "VITO"}
