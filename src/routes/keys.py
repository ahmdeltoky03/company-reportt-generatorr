from fastapi import APIRouter, HTTPException

from .schemas import APIKeysRequest

router = APIRouter(prefix="/api/keys", tags=["keys"])

# Store API keys in session (in-memory)
api_keys = {}


@router.post("/set")
async def set_api_keys(request: APIKeysRequest):
    """Set API keys for the session"""
    try:
        api_keys["cohere"] = request.cohere_api_key
        api_keys["tavily"] = request.tavily_api_key
        
        return {
            "status": "success",
            "message": "API keys set successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


def get_api_keys():
    """Get stored API keys"""
    return api_keys