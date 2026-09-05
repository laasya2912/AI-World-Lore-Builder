from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import get_db
from models import Lore

router = APIRouter(
    prefix="/lore",
    tags=["Lore"]
)


# -----------------------------
# Request Models
# -----------------------------

class LoreExpandRequest(BaseModel):
    world_id: int
    lore_type: str
    lore_name: str
    description: str


class LoreCreateRequest(BaseModel):
    world_id: int
    lore_type: str
    name: str
    description: str


class LoreUpdateRequest(BaseModel):
    name: str | None = None
    description: str | None = None
    facts: str | None = None
    relationships: str | None = None


# -----------------------------
# CREATE LORE
# -----------------------------

@router.post("/create")
def create_lore(
    request: LoreCreateRequest,
    db: Session = Depends(get_db)
):

    lore = Lore(
        world_id=request.world_id,
        type=request.lore_type,
        name=request.name,
        description=request.description
    )

    db.add(lore)
    db.commit()
    db.refresh(lore)

    return {
        "success": True,
        "message": "Lore created successfully!",
        "lore": {
            "id": lore.id,
            "world_id": lore.world_id,
            "type": lore.type,
            "name": lore.name,
            "description": lore.description
        }
    }


# -----------------------------
# EXPAND LORE
# -----------------------------

@router.post("/expand")
def expand_lore(
    request: LoreExpandRequest,
    db: Session = Depends(get_db)
):

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


# -----------------------------
# EDIT LORE
# -----------------------------

@router.put("/{lore_id}")
def update_lore(
    lore_id: int,
    request: LoreUpdateRequest,
    db: Session = Depends(get_db)
):

    lore = db.query(Lore).filter(Lore.id == lore_id).first()

    if not lore:
        raise HTTPException(
            status_code=404,
            detail="Lore not found"
        )

    if request.name is not None:
        lore.name = request.name

    if request.description is not None:
        lore.description = request.description

    if request.facts is not None:
        lore.facts = request.facts

    if request.relationships is not None:
        lore.relationships = request.relationships

    db.commit()
    db.refresh(lore)

    return {
        "success": True,
        "message": "Lore updated successfully!",
        "lore": {
            "id": lore.id,
            "world_id": lore.world_id,
            "type": lore.type,
            "name": lore.name,
            "description": lore.description,
            "facts": lore.facts,
            "relationships": lore.relationships
        }
    }
    # -----------------------------
# DELETE LORE
# -----------------------------

@router.delete("/{lore_id}")
def delete_lore(
    lore_id: int,
    db: Session = Depends(get_db)
):

    lore = db.query(Lore).filter(Lore.id == lore_id).first()

    if not lore:
        raise HTTPException(
            status_code=404,
            detail="Lore not found"
        )

    db.delete(lore)
    db.commit()

    return {
        "success": True,
        "message": "Lore deleted successfully!",
        "deleted_lore_id": lore_id
    }
    # -----------------------------
# CREATE BRANCH
# -----------------------------

class LoreBranchRequest(BaseModel):
    world_id: int
    lore_id: int
    new_description: str


@router.post("/branch")
def create_branch(
    request: LoreBranchRequest,
    db: Session = Depends(get_db)
):

    original_lore = (
        db.query(Lore)
        .filter(
            Lore.id == request.lore_id,
            Lore.world_id == request.world_id
        )
        .first()
    )

    if not original_lore:
        raise HTTPException(
            status_code=404,
            detail="Original lore not found"
        )

    # Demo branch world ID
    new_world_id = request.world_id + 1

    branch_lore = Lore(
        world_id=new_world_id,
        type=original_lore.type,
        name=original_lore.name,
        description=request.new_description,
        facts=original_lore.facts,
        relationships=original_lore.relationships
    )

    db.add(branch_lore)
    db.commit()
    db.refresh(branch_lore)

    return {
        "success": True,
        "message": "Alternate lore branch created successfully!",
        "original": {
            "world_id": original_lore.world_id,
            "lore_id": original_lore.id,
            "name": original_lore.name,
            "description": original_lore.description
        },
        "branch": {
            "world_id": branch_lore.world_id,
            "lore_id": branch_lore.id,
            "name": branch_lore.name,
            "description": branch_lore.description
        }
    }
    # -----------------------------
# GET ALL LORE
# -----------------------------

@router.get("/")
def get_all_lore(
    world_id: int = 1,
    db: Session = Depends(get_db)
):

    lore_items = (
        db.query(Lore)
        .filter(Lore.world_id == world_id)
        .all()
    )

    return {
        "success": True,
        "world_id": world_id,
        "count": len(lore_items),
        "lore": [
            {
                "id": lore.id,
                "type": lore.type,
                "name": lore.name,
                "description": lore.description,
                "facts": lore.facts,
                "relationships": lore.relationships,
                "created_at": lore.created_at,
                "updated_at": lore.updated_at
            }
            for lore in lore_items
        ]
    }