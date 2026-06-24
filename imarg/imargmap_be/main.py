from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers.forward import router as forward_router
from routers.reverse import router as reverse_router
from routers.auth import router as auth_router
from routers.aoi import router as aoi_router
from routers.payment import router as payment_router
from routers.download import router as download_router
from routers.user import router as user_router

app = FastAPI(
    title="FastAPI",
    description="Geocoding and Authentication API",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(auth_router)
app.include_router(forward_router)
app.include_router(reverse_router)
app.include_router(aoi_router)
app.include_router(payment_router)
app.include_router(download_router)
app.include_router(user_router)

@app.get("/", tags=["Root"])
def root():
    return {
        "success": True,
        "message": "API is running"
    }
