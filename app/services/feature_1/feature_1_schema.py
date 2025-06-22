# app/services/chatbot/chatbot_schema.py (CHANGED - simplified schemas, added update schema)

from typing import List, Optional
from datetime import datetime
from typing import Optional, List, Dict
from pydantic import BaseModel

class BulkInsertResponse(BaseModel):
    failed_items: Optional[List[Dict]] = None

class SystemInfoCreate(BaseModel):
    command_id: str
    command: str
    response: str
    category: str

class SystemInfoUpdate(BaseModel):
    command: Optional[str] = None
    response: Optional[str] = None
    category: Optional[str] = None

class SystemInfoResponse(BaseModel):
    command_id: str
    command: str
    response: str
    category: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    text_score: Optional[float] = None

class KeywordSearchQuery(BaseModel):
    keyword: str
    max_results: Optional[int] = 10

class SearchResponse(BaseModel):
    success: bool
    results: List[SystemInfoResponse]
    total_found: int
    message: Optional[str] = None

class BulkSystemInfo(BaseModel):
    system_info_list: List[SystemInfoCreate]

class BulkInsertResponse(BaseModel):
    success: bool
    message: str
    inserted_count: Optional[int] = None
    failed_items: Optional[List[Dict]] = None

class StandardResponse(BaseModel):
    success: bool
    message: str