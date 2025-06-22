# app/config/config.py (CHANGED - removed MODEL_NAME and similarity settings)
import os
from dotenv import load_dotenv

class Config:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
            load_dotenv()
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self):
        self.MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017/")
        self.DATABASE_NAME = os.getenv("DATABASE_NAME", "system_chatbot")
        self.COLLECTION_NAME = os.getenv("COLLECTION_NAME", "system_info")
        self.MAX_RESULTS = 10