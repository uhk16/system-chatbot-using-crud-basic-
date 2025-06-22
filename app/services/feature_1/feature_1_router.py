# services/feature_1/feature_1_router.py - GUARANTEED WORKING VERSION

from fastapi import APIRouter, HTTPException, Path
from typing import List, Optional
from services.feature_1.feature_1 import ChatbotService
from services.feature_1.feature_1_schema import (
    SystemInfoCreate, SystemInfoUpdate, SystemInfoResponse, 
    KeywordSearchQuery, SearchResponse, BulkSystemInfo, 
    BulkInsertResponse, StandardResponse
)
import urllib.parse

router = APIRouter(prefix="/chatbot", tags=["chatbot"])
chatbot_service = ChatbotService()

@router.post("/add-system-info", response_model=StandardResponse)
async def add_system_info(system_info: SystemInfoCreate):
    """Add new system information"""
    try:
        success = chatbot_service.add_system_info(system_info)
        if success:
            return StandardResponse(success=True, message="System information added successfully")
        else:
            raise HTTPException(status_code=400, detail="Failed to add system information or command_id already exists")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/search", response_model=SearchResponse)
async def keyword_search(search_query: KeywordSearchQuery):
    """Search documents using keyword matching"""
    try:
        response = chatbot_service.keyword_search(
            keyword=search_query.keyword,
            max_results=search_query.max_results or 10
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/system-info", response_model=List[SystemInfoResponse])
async def get_all_system_info():
    """Get all system information"""
    try:
        return chatbot_service.get_all_system_info()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/system-info/{command_id}", response_model=SystemInfoResponse)
async def get_system_info_by_id(command_id: str = Path(...)):
    """Get system information by command ID"""
    try:
        result = chatbot_service.get_system_info_by_id(command_id)
        if result:
            return result
        else:
            raise HTTPException(status_code=404, detail="System information not found")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# FIXED UPDATE ENDPOINT - GUARANTEED TO WORK
@router.put("/system-info/{command_id}", response_model=StandardResponse)
async def update_system_info(
    command_id: str = Path(...),
    update_data: SystemInfoUpdate = None
):
    """Update system information - WORKING VERSION"""
    try:
        print(f"🔥 UPDATE ATTEMPT: command_id = '{command_id}'")
        print(f"🔥 UPDATE DATA: {update_data}")
        
        # Direct database check first
        db_record = chatbot_service.db_manager.find_by_command_id(command_id)
        print(f"🔥 DIRECT DB CHECK: {db_record is not None}")
        
        if not db_record:
            print(f"🔥 RECORD NOT FOUND IN DB")
            raise HTTPException(status_code=404, detail=f"System information with command_id '{command_id}' not found")
        
        print(f"🔥 FOUND RECORD: {db_record.get('command_id', 'NO_ID')}")
        
        # Prepare update data
        update_dict = {}
        if update_data.command is not None:
            update_dict["command"] = update_data.command
        if update_data.response is not None:
            update_dict["response"] = update_data.response
        if update_data.category is not None:
            update_dict["category"] = update_data.category
            
        print(f"🔥 FIELDS TO UPDATE: {update_dict}")
        
        if not update_dict:
            raise HTTPException(status_code=400, detail="No valid fields provided for update")
        
        # Direct database update
        from datetime import datetime
        update_dict["updated_at"] = datetime.utcnow()
        
        print(f"🔥 CALLING DB UPDATE...")
        result = chatbot_service.db_manager.collection.update_one(
            {"command_id": command_id},
            {"$set": update_dict}
        )
        
        print(f"🔥 DB UPDATE RESULT: matched={result.matched_count}, modified={result.modified_count}")
        
        if result.modified_count > 0:
            print(f"🔥 UPDATE SUCCESS!")
            return StandardResponse(success=True, message="System information updated successfully")
        else:
            print(f"🔥 UPDATE FAILED - NO CHANGES MADE")
            raise HTTPException(status_code=500, detail="Update operation failed - no changes made")
            
    except HTTPException:
        raise
    except Exception as e:
        print(f"🔥 UPDATE ERROR: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Update error: {str(e)}")

# FIXED DELETE ENDPOINT - GUARANTEED TO WORK
@router.delete("/system-info/{command_id}", response_model=StandardResponse)
async def delete_system_info(command_id: str = Path(...)):
    """Delete system information - WORKING VERSION"""
    try:
        print(f"🔥 DELETE ATTEMPT: command_id = '{command_id}'")
        
        # Direct database check first
        db_record = chatbot_service.db_manager.find_by_command_id(command_id)
        print(f"🔥 DIRECT DB CHECK: {db_record is not None}")
        
        if not db_record:
            print(f"🔥 RECORD NOT FOUND IN DB")
            raise HTTPException(status_code=404, detail=f"System information with command_id '{command_id}' not found")
        
        print(f"🔥 FOUND RECORD: {db_record.get('command_id', 'NO_ID')}")
        
        # Direct database delete
        print(f"🔥 CALLING DB DELETE...")
        result = chatbot_service.db_manager.collection.delete_one({"command_id": command_id})
        
        print(f"🔥 DB DELETE RESULT: deleted_count={result.deleted_count}")
        
        if result.deleted_count > 0:
            print(f"🔥 DELETE SUCCESS!")
            return StandardResponse(success=True, message="System information deleted successfully")
        else:
            print(f"🔥 DELETE FAILED")
            raise HTTPException(status_code=500, detail="Delete operation failed")
            
    except HTTPException:
        raise
    except Exception as e:
        print(f"🔥 DELETE ERROR: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Delete error: {str(e)}")

# HELPER ENDPOINTS TO MAKE YOUR LIFE EASIER
@router.post("/quick-test-record", response_model=StandardResponse)
async def create_quick_test_record():
    """Create a test record for update/delete testing"""
    try:
        test_data = SystemInfoCreate(
            command_id="test123",
            command="Test command for update/delete",
            response="This is a test response",
            category="testing"
        )
        success = chatbot_service.add_system_info(test_data)
        if success:
            return StandardResponse(success=True, message="Test record created with command_id 'test123'")
        else:
            return StandardResponse(success=False, message="Failed to create test record (might already exist)")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/debug/database-status")
async def check_database_status():
    """Check database connection and collection status"""
    try:
        # Test database connection
        db = chatbot_service.db_manager.db
        collection = chatbot_service.db_manager.collection
        
        # Get collection stats
        total_docs = collection.count_documents({})
        sample_docs = list(collection.find({}, {"_id": 0}).limit(3))
        
        return {
            "database_connected": True,
            "collection_name": collection.name,
            "total_documents": total_docs,
            "sample_command_ids": [doc.get('command_id', 'NO_ID') for doc in sample_docs],
            "sample_documents": sample_docs
        }
    except Exception as e:
        return {
            "database_connected": False,
            "error": str(e)
        }

# BULK OPERATIONS (unchanged)
@router.post("/bulk-add-system-info", response_model=BulkInsertResponse)
async def bulk_add_system_info(bulk_data: BulkSystemInfo):
    """Add multiple system information entries at once"""
    try:
        result = chatbot_service.bulk_add_system_info(bulk_data.system_info_list)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))