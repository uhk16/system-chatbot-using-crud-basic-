# main.py (CHANGED - updated description and version)
from fastapi import FastAPI
from services.feature_1.feature_1_router import router as chatbot_router
from database.database_connection import DatabaseConnection

app = FastAPI(
    title="System Chatbot API",
    description="A keyword search-based chatbot for system information with CRUD operations",
    version="1.0.0"
)

# Include routers
app.include_router(chatbot_router)

@app.get("/")
async def root():
    return {"message": "System Chatbot API v1.0 is running with keyword search"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "API is operational"}

@app.on_event("shutdown")
async def shutdown_event():
    DatabaseConnection.close_connection()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)