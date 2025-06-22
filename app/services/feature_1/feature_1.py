# services/feature_1/feature_1.py (FIXED ChatbotService)
from typing import List, Dict, Optional
from database.database_manager import DatabaseManager  # Adjusted to relative import
from config.config import Config  # Adjust import path
from services.feature_1.feature_1_schema import (
    SystemInfoCreate, SystemInfoUpdate, SystemInfoResponse, 
    SearchResponse, BulkInsertResponse
)
from datetime import datetime

class ChatbotService:
    def __init__(self):
        self.config = Config()
        self.db_manager = DatabaseManager()
    
    def add_system_info(self, system_info: SystemInfoCreate) -> bool:
        """Add new system information"""
        try:
            # Check if command_id already exists
            existing = self.db_manager.find_by_command_id(system_info.command_id)
            if existing:
                return False
            
            # FIXED: Call insert_system_info without vector parameter
            return self.db_manager.insert_system_info(
                command_id=system_info.command_id,
                command=system_info.command,
                response=system_info.response,
                category=system_info.category
            )
        except Exception as e:
            print(f"Add system info error: {e}")
            return False
    
    def keyword_search(self, keyword: str, max_results: int = 10) -> SearchResponse:
        """Search for documents using keyword matching"""
        try:
            if not keyword.strip():
                return SearchResponse(
                    success=False,
                    results=[],
                    total_found=0,
                    message="Please provide a valid keyword."
                )
            
            results = self.db_manager.search_by_keyword(keyword, limit=max_results)
            
            response_list = []
            for doc in results:
                try:
                    response_list.append(SystemInfoResponse(
                        command_id=doc['command_id'],
                        command=doc['command'],
                        response=doc['response'],
                        category=doc['category'],
                        created_at=doc.get('created_at'),
                        updated_at=doc.get('updated_at'),
                        text_score=doc.get('score', 0.0)
                    ))
                except Exception as validation_error:
                    print(f"Validation error for doc {doc.get('command_id', 'unknown')}: {validation_error}")
                    continue
            
            if response_list:
                return SearchResponse(
                    success=True,
                    results=response_list,
                    total_found=len(response_list)
                )
            else:
                return SearchResponse(
                    success=False,
                    results=[],
                    total_found=0,
                    message="No results found for your keyword."
                )
            
        except Exception as e:
            print(f"Keyword search error: {e}")
            return SearchResponse(
                success=False,
                results=[],
                total_found=0,
                message=str(e)
            )
    
    def get_system_info_by_id(self, command_id: str) -> Optional[SystemInfoResponse]:
        """Get system information by command ID"""
        try:
            result = self.db_manager.find_by_command_id(command_id)
            if result:
                return SystemInfoResponse(
                    command_id=result['command_id'],
                    command=result['command'],
                    response=result['response'],
                    category=result['category'],
                    created_at=result.get('created_at'),
                    updated_at=result.get('updated_at')
                )
            return None
        except Exception as e:
            print(f"Get system info by ID error: {e}")
            return None
    
    def get_all_system_info(self) -> List[SystemInfoResponse]:
        """Get all system information"""
        try:
            results = self.db_manager.get_all_system_info()
            response_list = []
            for doc in results:
                try:
                    response_list.append(SystemInfoResponse(
                        command_id=doc['command_id'],
                        command=doc['command'],
                        response=doc['response'],
                        category=doc['category'],
                        created_at=doc.get('created_at'),
                        updated_at=doc.get('updated_at')
                    ))
                except Exception as validation_error:
                    print(f"Validation error for doc {doc.get('command_id', 'unknown')}: {validation_error}")
                    continue
            return response_list
        except Exception as e:
            print(f"Get all system info error: {e}")
            return []
    
    def update_system_info(self, command_id: str, update_data: SystemInfoUpdate) -> bool:
        """Update system information"""
        try:
            # Convert Pydantic model to dict, excluding None values
            update_dict = {k: v for k, v in update_data.dict().items() if v is not None}
            
            if not update_dict:
                return False
            
            return self.db_manager.update_system_info(command_id, update_dict)
        except Exception as e:
            print(f"Update system info error: {e}")
            return False
    
    def delete_system_info(self, command_id: str) -> bool:
        """Delete system information"""
        try:
            return self.db_manager.delete_system_info(command_id)
        except Exception as e:
            print(f"Delete system info error: {e}")
            return False
    
    def bulk_add_system_info(self, bulk_data: List[SystemInfoCreate]) -> BulkInsertResponse:
        """Add multiple system information entries at once"""
        try:
            if not bulk_data:
                return BulkInsertResponse(
                    success=False,
                    message="No data provided",
                    inserted_count=0,
                    failed_items=[]
                )
            
            documents_to_insert = []
            failed_items = []
            
            for item in bulk_data:
                try:
                    # Check if command_id already exists
                    existing = self.db_manager.find_by_command_id(item.command_id)
                    if existing:
                        failed_items.append({
                            "command_id": item.command_id,
                            "reason": "Command ID already exists"
                        })
                        continue
                    
                    document = {
                        "command_id": item.command_id,
                        "command": item.command,
                        "response": item.response,
                        "category": item.category,
                        "created_at": datetime.utcnow(),
                        "updated_at": datetime.utcnow()
                    }
                    documents_to_insert.append(document)
                    
                except Exception as e:
                    failed_items.append({
                        "command_id": getattr(item, 'command_id', 'unknown'),
                        "reason": str(e)
                    })
            
            # Bulk insert successful documents
            if documents_to_insert:
                insert_result = self.db_manager.bulk_insert_system_info(documents_to_insert)
                if insert_result["success"]:
                    return BulkInsertResponse(
                        success=True,
                        message=f"Successfully inserted {insert_result['inserted_count']} documents",
                        inserted_count=insert_result["inserted_count"],
                        failed_items=failed_items
                    )
                else:
                    return BulkInsertResponse(
                        success=False,
                        message=f"Bulk insert failed: {insert_result['message']}",
                        inserted_count=0,
                        failed_items=failed_items
                    )
            else:
                return BulkInsertResponse(
                    success=False,
                    message="No valid documents to insert",
                    inserted_count=0,
                    failed_items=failed_items
                )
                
        except Exception as e:
            print(f"Bulk add system info error: {e}")
            return BulkInsertResponse(
                success=False,
                message=str(e),
                inserted_count=0,
                failed_items=[]
            )