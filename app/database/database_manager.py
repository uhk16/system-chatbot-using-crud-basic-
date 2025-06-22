# services/feature_1/feature_1_database_manager.py (FIXED)
from typing import List, Dict, Optional
from database.database_connection import DatabaseConnection  # Adjust import path as needed
from config.config import Config  # Adjust import path as needed
from datetime import datetime

class DatabaseManager:
    def __init__(self):
        self.config = Config()
        self.db = DatabaseConnection.get_database()
        self.collection = self.db[self.config.COLLECTION_NAME]
        self._create_indexes()
    
    def _create_indexes(self):
        """Create necessary indexes for efficient querying"""
        try:
            self.collection.create_index("command_id", unique=True)
            self.collection.create_index("category")
            # Add text index for keyword search
            self.collection.create_index([("command", "text"), ("response", "text"), ("category", "text")])
        except Exception as e:
            print(f"Index creation error: {e}")
    
    def insert_system_info(self, command_id: str, command: str, response: str, category: str) -> bool:
        """Insert system information (FIXED - removed vector parameter)"""
        try:
            document = {
                "command_id": command_id,
                "command": command,
                "response": response,
                "category": category,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            }
            result = self.collection.insert_one(document)
            return bool(result.inserted_id)
        except Exception as e:
            print(f"Insert error: {e}")
            return False
    
    def search_by_keyword(self, keyword: str, limit: int = None) -> List[Dict]:
        """Search documents by keyword using text search"""
        try:
            query = {"$text": {"$search": keyword}}
            projection = {"_id": 0, "score": {"$meta": "textScore"}}
            
            cursor = self.collection.find(query, projection).sort([("score", {"$meta": "textScore"})])
            
            if limit:
                cursor = cursor.limit(limit)
            
            results = list(cursor)
            
            # Fix datetime issues - ensure proper datetime objects
            for result in results:
                if 'created_at' in result and not isinstance(result['created_at'], datetime):
                    if isinstance(result['created_at'], dict):
                        result['created_at'] = datetime.utcnow()  # Fallback for invalid data
                if 'updated_at' in result and not isinstance(result['updated_at'], datetime):
                    if isinstance(result['updated_at'], dict):
                        result['updated_at'] = datetime.utcnow()  # Fallback for invalid data
            
            return results
        except Exception as e:
            print(f"Keyword search error: {e}")
            return []
    
    def find_by_command_id(self, command_id: str) -> Optional[Dict]:
        """Find document by command ID"""
        try:
            result = self.collection.find_one({"command_id": command_id}, {"_id": 0})
            
            # Fix datetime issues if found
            if result:
                if 'created_at' in result and not isinstance(result['created_at'], datetime):
                    if isinstance(result['created_at'], dict):
                        result['created_at'] = datetime.utcnow()
                if 'updated_at' in result and not isinstance(result['updated_at'], datetime):
                    if isinstance(result['updated_at'], dict):
                        result['updated_at'] = datetime.utcnow()
            
            return result
        except Exception as e:
            print(f"Find error: {e}")
            return None
    
    def update_system_info(self, command_id: str, update_data: Dict) -> bool:
        """Update system information"""
        try:
            update_data["updated_at"] = datetime.utcnow()
            result = self.collection.update_one(
                {"command_id": command_id},
                {"$set": update_data}
            )
            return result.modified_count > 0
        except Exception as e:
            print(f"Update error: {e}")
            return False
    
    def delete_system_info(self, command_id: str) -> bool:
        """Delete system information"""
        try:
            result = self.collection.delete_one({"command_id": command_id})
            return result.deleted_count > 0
        except Exception as e:
            print(f"Delete error: {e}")
            return False
    
    def get_all_system_info(self) -> List[Dict]:
        """Get all system information"""
        try:
            results = list(self.collection.find({}, {"_id": 0}))
            
            # Fix datetime issues for all results
            for result in results:
                if 'created_at' in result and not isinstance(result['created_at'], datetime):
                    if isinstance(result['created_at'], dict):
                        result['created_at'] = datetime.utcnow()
                if 'updated_at' in result and not isinstance(result['updated_at'], datetime):
                    if isinstance(result['updated_at'], dict):
                        result['updated_at'] = datetime.utcnow()
            
            return results
        except Exception as e:
            print(f"Get all error: {e}")
            return []
    
    def bulk_insert_system_info(self, documents: List[Dict]) -> Dict:
        """Bulk insert multiple system information documents"""
        try:
            if not documents:
                return {"success": False, "message": "No documents provided"}
            
            # Ensure all documents have proper datetime objects
            for doc in documents:
                if 'created_at' not in doc:
                    doc['created_at'] = datetime.utcnow()
                if 'updated_at' not in doc:
                    doc['updated_at'] = datetime.utcnow()
            
            result = self.collection.insert_many(documents)
            return {
                "success": True,
                "inserted_count": len(result.inserted_ids),
                "inserted_ids": [str(id) for id in result.inserted_ids]
            }
        except Exception as e:
            print(f"Bulk insert error: {e}")
            return {"success": False, "message": str(e)}
