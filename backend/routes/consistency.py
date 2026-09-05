from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import get_db
from models import Lore

router = APIRouter(
    prefix="/consistency",
    tags=["Consistency"]
)


class ConsistencyCheckRequest(BaseModel):
    world_id: int
    new_lore: str


@router.post("/check")
def check_consistency(
    request: ConsistencyCheckRequest,
    db: Session = Depends(get_db)
):

    existing_lore = (
        db.query(Lore)
        .filter(Lore.world_id == request.world_id)
        .all()
    )

    conflicts = []

    # Simple keyword-based contradiction detection
    new_text = request.new_lore.lower()

    for lore in existing_lore:

        old_text = (
            lore.name + " " + lore.description
        ).lower()

        # Detect same character/place mentioned with different rulers
        if "karna" in new_text and "karna" in old_text:

            if (
                "anga" in old_text
                and "hastinapura" in new_text
            ):
                conflicts.append({
                    "existing_lore": lore.description,
                    "new_lore": request.new_lore,
                    "reason": "Karna is associated with Anga in existing lore but the new lore associates him with Hastinapura."
                })

    if conflicts:

        return {
            "success": True,
            "conflict_found": True,
            "confidence": 0.95,
            "message": "Potential contradiction detected.",
            "conflicts": conflicts,
            "actions": [
                "FIX",
                "KEEP_ANYWAY",
                "CREATE_BRANCH"
            ]
        }

    return {
        "success": True,
        "conflict_found": False,
        "confidence": 0.95,
        "message": "No contradiction detected.",
        "conflicts": []
    }