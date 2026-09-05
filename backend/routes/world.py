from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from schemas import WorldGenerateRequest
from ai_service import generate_world
from database import get_db
from models import Lore

router = APIRouter(
    prefix="/world",
    tags=["World"]
)


@router.post("/generate")
def generate_world_api(
    request: WorldGenerateRequest,
    db: Session = Depends(get_db)
):

    result = generate_world(
        request.genre,
        request.tone,
        request.concept
    )

    # Save generated lore into database
    lore_items = []

    for region in result["regions"]:
        lore = Lore(
            world_id=1,
            type="REGION",
            name=region["name"],
            description=region["description"]
        )
        db.add(lore)
        lore_items.append(lore)

    for faction in result["factions"]:
        lore = Lore(
            world_id=1,
            type="FACTION",
            name=faction["name"],
            description=faction["description"]
        )
        db.add(lore)
        lore_items.append(lore)

    for character in result["characters"]:
        lore = Lore(
            world_id=1,
            type="CHARACTER",
            name=character["name"],
            description=character["description"]
        )
        db.add(lore)
        lore_items.append(lore)

    for event in result["events"]:
        lore = Lore(
            world_id=1,
            type="EVENT",
            name=event["name"],
            description=event["description"]
        )
        db.add(lore)
        lore_items.append(lore)

    db.commit()

    return {
        "success": True,
        "message": "World generated and saved successfully!",
        "world": result
    }