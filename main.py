import os
from typing import Optional, List
from uuid import UUID
from dotenv import load_dotenv
from fastapi import FastAPI, Depends, Header, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import httpx
import uvicorn

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
ANON_KEY = os.getenv("SUPABASE_ANON_KEY")
TABLE = os.getenv("TABLE_VTUBERS", "vtubers")
POSTGREST_URL = f"{SUPABASE_URL}/rest/v1"

if not SUPABASE_URL or not ANON_KEY:
    raise RuntimeError("SUPABASE_URL or SUPABASE_ANON_KEY not found.")

app = FastAPI(
    title="VTuber Wiki API",
    description="A public API for VTuber information and profiles",
    version="1.0.0"
)

# Add CORS middleware for Postman testing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# VTuber Models
class VTuberCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    agency: Optional[str] = Field(default=None, max_length=100)
    debut_date: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = None
    youtube_channel: Optional[str] = None
    twitter_handle: Optional[str] = None
    tags: Optional[List[str]] = None

class VTuberUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=100)
    agency: Optional[str] = None
    debut_date: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = None
    youtube_channel: Optional[str] = None
    twitter_handle: Optional[str] = None
    tags: Optional[List[str]] = None

class VTuberOut(BaseModel):
    id: UUID
    name: str
    agency: Optional[str]
    debut_date: Optional[str]
    description: Optional[str]
    image_url: Optional[str]
    youtube_channel: Optional[str]
    twitter_handle: Optional[str]
    tags: Optional[List[str]]
    created_at: str
    updated_at: str

class VTuberBulkCreate(BaseModel):
    vtubers: List[VTuberCreate]

# Authentication dependencies
async def get_user_token(authorization: Optional[str] = Header(default=None)):
    """Required for write operations"""
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid Authorization header. Required for this operation."
        )
    return authorization

def postgrest_headers(user_authorization: Optional[str] = None):
    """Headers for Supabase requests"""
    headers = {
        "apikey": ANON_KEY,
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Prefer": "return=representation",
    }
    if user_authorization:
        headers["Authorization"] = user_authorization
    return headers

# Public endpoints (no authentication required)
@app.get("/")
async def root():
    return {
        "message": "Welcome to VTuber Wiki API",
        "version": "1.0.0",
        "endpoints": {
            "public": [
                "GET /vtubers - List all VTubers",
                "GET /vtubers/{id} - Get VTuber by ID",
                "GET /search - Search VTubers",
                "GET /agencies - List all agencies"
            ],
            "protected": [
                "POST /vtubers - Create new VTuber (requires auth)",
                "POST /vtubers/bulk - Create multiple VTubers (requires auth)",
                "POST /vtubers/batch - Create multiple VTubers (direct array) (requires auth)",
                "PUT /vtubers/{id} - Update VTuber (requires auth)",
                "DELETE /vtubers/{id} - Delete VTuber (requires auth)"
            ]
        }
    }

@app.get("/health")
async def health():
    return {"status": "ok", "service": "VTuber Wiki API"}

@app.get("/vtubers", response_model=List[VTuberOut])
async def list_vtubers(
    limit: int = 50,
    offset: int = 0,
    agency: Optional[str] = None,
    sort_by: str = "name"
):
    """Get all VTubers (public endpoint)"""
    params = {
        "select": "*",
        "limit": str(min(limit, 100)),
        "offset": str(max(offset, 0)),
        "order": f"{sort_by}.asc"
    }
    
    if agency:
        params["agency"] = f"eq.{agency}"
    
    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.get(
            f"{POSTGREST_URL}/{TABLE}",
            headers=postgrest_headers(),  # No auth required
            params=params
        )
    
    if r.status_code >= 400:
        raise HTTPException(r.status_code, r.text)
    return r.json()

@app.get("/vtubers/{vtuber_id}", response_model=List[VTuberOut])
async def get_vtuber(vtuber_id: UUID):
    """Get specific VTuber by ID (public endpoint)"""
    params = {"select": "*", "id": f"eq.{vtuber_id}"}
    
    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.get(
            f"{POSTGREST_URL}/{TABLE}",
            headers=postgrest_headers(),  # No auth required
            params=params
        )
    
    if r.status_code >= 400:
        raise HTTPException(r.status_code, r.text)
    
    result = r.json()
    if not result:
        raise HTTPException(status_code=404, detail="VTuber not found")
    return result

@app.get("/search", response_model=List[VTuberOut])
async def search_vtubers(
    q: str,
    limit: int = 20,
    offset: int = 0
):
    """Search VTubers by name or description (public endpoint)"""
    params = {
        "select": "*",
        "limit": str(min(limit, 50)),
        "offset": str(max(offset, 0)),
        "or": f"(name.ilike.*{q}*,description.ilike.*{q}*)"
    }
    
    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.get(
            f"{POSTGREST_URL}/{TABLE}",
            headers=postgrest_headers(),  # No auth required
            params=params
        )
    
    if r.status_code >= 400:
        raise HTTPException(r.status_code, r.text)
    return r.json()

@app.get("/agencies")
async def list_agencies():
    """Get list of all agencies (public endpoint)"""
    params = {
        "select": "agency",
        "agency": "not.is.null",
        "order": "agency.asc"
    }
    
    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.get(
            f"{POSTGREST_URL}/{TABLE}",
            headers=postgrest_headers(),  # No auth required
            params=params
        )
    
    if r.status_code >= 400:
        raise HTTPException(r.status_code, r.text)
    
    agencies = list(set([item["agency"] for item in r.json() if item["agency"]]))
    return {"agencies": sorted(agencies)}

# Protected endpoints (require authentication)
@app.post("/vtubers", response_model=List[VTuberOut], status_code=201)
async def create_vtuber(payload: VTuberCreate, auth=Depends(get_user_token)):
    """Create a new VTuber entry (requires authentication)"""
    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.post(
            f"{POSTGREST_URL}/{TABLE}",
            headers=postgrest_headers(auth),
            json=payload.model_dump(mode="json")
        )
        
    if r.status_code >= 400:
        raise HTTPException(r.status_code, r.text)
    return r.json()

@app.post("/vtubers/bulk", response_model=List[VTuberOut], status_code=201)
async def create_vtubers_bulk(payload: VTuberBulkCreate, auth=Depends(get_user_token)):
    """Create multiple VTubers in bulk (requires authentication)"""
    async with httpx.AsyncClient(timeout=30) as client:
        results = []
        for vtuber_data in payload.vtubers:
            r = await client.post(
                f"{POSTGREST_URL}/{TABLE}",
                headers=postgrest_headers(auth),
                json=vtuber_data.model_dump(mode="json")
            )
            if r.status_code >= 400:
                continue
            results.extend(r.json())
        return results

@app.post("/vtubers/batch", response_model=List[VTuberOut], status_code=201)
async def create_vtubers_batch(vtubers: List[VTuberCreate], auth=Depends(get_user_token)):
    """Create multiple VTubers in batch (direct array format) (requires authentication)"""
    async with httpx.AsyncClient(timeout=30) as client:
        results = []
        for vtuber_data in vtubers:
            r = await client.post(
                f"{POSTGREST_URL}/{TABLE}",
                headers=postgrest_headers(auth),
                json=vtuber_data.model_dump(mode="json")
            )
            if r.status_code >= 400:
                continue
            results.extend(r.json())
        return results

@app.put("/vtubers/{vtuber_id}", response_model=List[VTuberOut])
async def update_vtuber(vtuber_id: UUID, payload: VTuberUpdate, auth=Depends(get_user_token)):
    """Update VTuber information (requires authentication)"""
    data = {k: v for k, v in payload.model_dump(mode="json").items() if v is not None}
    
    if not data:
        raise HTTPException(400, "No fields to update")
    
    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.patch(
            f"{POSTGREST_URL}/{TABLE}",
            headers=postgrest_headers(auth),
            params={"id": f"eq.{vtuber_id}"},
            json=data,
        )
    
    if r.status_code >= 400:
        raise HTTPException(r.status_code, r.text)
    
    result = r.json()
    if not result:
        raise HTTPException(status_code=404, detail="VTuber not found")
    return result

@app.delete("/vtubers/{vtuber_id}", status_code=204)
async def delete_vtuber(vtuber_id: UUID, auth=Depends(get_user_token)):
    """Delete a VTuber entry (requires authentication)"""
    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.delete(
            f"{POSTGREST_URL}/{TABLE}",
            headers=postgrest_headers(auth),
            params={"id": f"eq.{vtuber_id}"},
        )
    
    if r.status_code >= 400:
        raise HTTPException(r.status_code, r.text)
    return {}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)