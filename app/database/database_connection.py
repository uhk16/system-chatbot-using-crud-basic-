# app/database/database_connection.py
from pymongo import MongoClient
from config.config import Config

class DatabaseConnection:
    _client = None
    _db = None
    
    @classmethod
    def get_client(cls):
        if cls._client is None:
            config = Config()
            cls._client = MongoClient(config.MONGODB_URI)
        return cls._client
    
    @classmethod
    def get_database(cls):
        if cls._db is None:
            config = Config()
            client = cls.get_client()
            cls._db = client[config.DATABASE_NAME]
        return cls._db
    
    @classmethod
    def close_connection(cls):
        if cls._client:
            cls._client.close()
            cls._client = None
            cls._db = None