from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import chat, predict
from services.chat_service import init_chat_service
from services.prediction_service import load_model
import contextlib

@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup event
    print("Initializing services...")
    init_chat_service()
    load_model()
    yield
    # Shutdown event
    print("Shutting down...")

app = FastAPI(title="PMOS Backend", lifespan=lifespan)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(chat.router, prefix="/api/chat", tags=["Chat"])
app.include_router(predict.router, prefix="/api/predict", tags=["Predict"])

@app.get("/")
def root():
    return {"message": "Welcome to the PMOS Project Backend"}
