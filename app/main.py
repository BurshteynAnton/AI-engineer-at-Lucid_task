from fastapi import FastAPI
from app.controllers.auth_controller import router as auth_router
from app.controllers.post_controller import router as post_router
from app.core.config import settings

app = FastAPI(
    title=settings.project_name,
    debug=settings.debug,
    openapi_url=f"{settings.api_v1_prefix}/openapi.json"
)

app.include_router(
    auth_router,
    prefix=settings.api_v1_prefix,
    tags=["Users & Authentication"]
)

app.include_router(
    post_router,
    prefix=settings.api_v1_prefix,
    tags=["Posts"]
)

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI Blog API! See /docs for API documentation."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
