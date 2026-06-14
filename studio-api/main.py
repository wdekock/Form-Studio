import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from studio_node import form_studio_node_api

app = FastAPI(title="State-Driven Form Engine Core")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(form_studio_node_api, prefix="/api/v1")

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
