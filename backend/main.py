from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from database import engine, Base, get_db
import models


# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI World Lore Builder API",
    description="Backend API for persistent fantasy world lore",
    version="1.0"
)


# =========================================================
# PYDANTIC SCHEMAS
# =========================================================

class WorldCreate(BaseModel):
    name: str
    genre: str | None = None
    tone: str | None = None


class LoreCreate(BaseModel):
    world_id: int
    type: str
    name: str
    description: str | None = None
    metadata_json: str | None = None


class RelationshipCreate(BaseModel):
    source_id: int
    target_id: int
    relationship_type: str


class BranchCreate(BaseModel):
    world_id: int
    parent_lore_id: int | None = None
    name: str
    description: str | None = None


# =========================================================
# HOME
# =========================================================

@app.get("/")
def home():
    return {
        "message": "AI World Lore Builder API is running",
        "status": "success"
    }


# =========================================================
# WORLD CRUD
# =========================================================

@app.post("/worlds")
def create_world(
    world_data: WorldCreate,
    db: Session = Depends(get_db)
):
    world = models.World(
        name=world_data.name,
        genre=world_data.genre,
        tone=world_data.tone
    )

    db.add(world)
    db.commit()
    db.refresh(world)

    return world


@app.get("/worlds")
def get_worlds(
    db: Session = Depends(get_db)
):
    return db.query(models.World).all()


@app.get("/worlds/{world_id}")
def get_world(
    world_id: int,
    db: Session = Depends(get_db)
):
    world = db.query(models.World).filter(
        models.World.id == world_id
    ).first()

    if not world:
        raise HTTPException(
            status_code=404,
            detail="World not found"
        )

    return world


@app.delete("/worlds/{world_id}")
def delete_world(
    world_id: int,
    db: Session = Depends(get_db)
):
    world = db.query(models.World).filter(
        models.World.id == world_id
    ).first()

    if not world:
        raise HTTPException(
            status_code=404,
            detail="World not found"
        )

    db.delete(world)
    db.commit()

    return {
        "message": "World deleted successfully"
    }


# =========================================================
# LORE CRUD
# =========================================================

@app.post("/lore")
def create_lore(
    lore_data: LoreCreate,
    db: Session = Depends(get_db)
):
    world = db.query(models.World).filter(
        models.World.id == lore_data.world_id
    ).first()

    if not world:
        raise HTTPException(
            status_code=404,
            detail="World not found"
        )

    lore = models.Lore(
        world_id=lore_data.world_id,
        type=lore_data.type,
        name=lore_data.name,
        description=lore_data.description,
        metadata_json=lore_data.metadata_json
    )

    db.add(lore)
    db.commit()
    db.refresh(lore)

    return lore


@app.get("/lore")
def get_all_lore(
    db: Session = Depends(get_db)
):
    return db.query(models.Lore).all()


@app.get("/worlds/{world_id}/lore")
def get_world_lore(
    world_id: int,
    db: Session = Depends(get_db)
):
    return db.query(models.Lore).filter(
        models.Lore.world_id == world_id
    ).all()


@app.get("/lore/{lore_id}")
def get_lore(
    lore_id: int,
    db: Session = Depends(get_db)
):
    lore = db.query(models.Lore).filter(
        models.Lore.id == lore_id
    ).first()

    if not lore:
        raise HTTPException(
            status_code=404,
            detail="Lore not found"
        )

    return lore


@app.put("/lore/{lore_id}")
def update_lore(
    lore_id: int,
    lore_data: LoreCreate,
    db: Session = Depends(get_db)
):
    lore = db.query(models.Lore).filter(
        models.Lore.id == lore_id
    ).first()

    if not lore:
        raise HTTPException(
            status_code=404,
            detail="Lore not found"
        )

    lore.type = lore_data.type
    lore.name = lore_data.name
    lore.description = lore_data.description
    lore.metadata_json = lore_data.metadata_json

    db.commit()
    db.refresh(lore)

    return lore


@app.delete("/lore/{lore_id}")
def delete_lore(
    lore_id: int,
    db: Session = Depends(get_db)
):
    lore = db.query(models.Lore).filter(
        models.Lore.id == lore_id
    ).first()

    if not lore:
        raise HTTPException(
            status_code=404,
            detail="Lore not found"
        )

    db.delete(lore)
    db.commit()

    return {
        "message": "Lore deleted successfully"
    }


# =========================================================
# RELATIONSHIPS
# =========================================================

@app.post("/relationships")
def create_relationship(
    relationship_data: RelationshipCreate,
    db: Session = Depends(get_db)
):
    relationship = models.LoreRelationship(
        source_id=relationship_data.source_id,
        target_id=relationship_data.target_id,
        relationship_type=relationship_data.relationship_type
    )

    db.add(relationship)
    db.commit()
    db.refresh(relationship)

    return relationship


@app.get("/relationships")
def get_relationships(
    db: Session = Depends(get_db)
):
    return db.query(
        models.LoreRelationship
    ).all()


# =========================================================
# BRANCHES
# =========================================================

@app.post("/branches")
def create_branch(
    branch_data: BranchCreate,
    db: Session = Depends(get_db)
):
    branch = models.LoreBranch(
        world_id=branch_data.world_id,
        parent_lore_id=branch_data.parent_lore_id,
        name=branch_data.name,
        description=branch_data.description
    )

    db.add(branch)
    db.commit()
    db.refresh(branch)

    return branch


@app.get("/branches")
def get_branches(
    db: Session = Depends(get_db)
):
    return db.query(models.LoreBranch).all()