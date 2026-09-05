from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(
    prefix="/consistency",
    tags=["Consistency"]
)


class ConsistencyCheckRequest(BaseModel):
    world_id: int
    new_lore: str


@router.post("/check")
def check_consistency(request: ConsistencyCheckRequest):

    # Temporary mock consistency checker
    conflict_found = False

    return {
        "success": True,
        "world_id": request.world_id,
        "conflict_found": conflict_found,
        "confidence": 0.95,
        "message": "No contradiction detected.",
        "new_lore": request.new_lore
    }