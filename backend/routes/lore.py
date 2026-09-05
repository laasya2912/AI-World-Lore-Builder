from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(
    prefix="/lore",
    tags=["Lore"]
)


class LoreExpandRequest(BaseModel):
    world_id: int
    lore_type: str
    lore_name: str
    description: str


@router.post("/expand")
def expand_lore(request: LoreExpandRequest):

    return {
        "success": True,
        "message": "Lore expansion generated successfully!",
        "parent": {
            "type": request.lore_type,
            "name": request.lore_name,
            "description": request.description
        },
        "expanded_lore": {
            "type": "CHARACTER",
            "name": f"{request.lore_name} - Expanded Lore",
            "description": (
                f"Additional lore connected to {request.lore_name}. "
                "This can later be generated using the GenAI service."
            )
        }
    }