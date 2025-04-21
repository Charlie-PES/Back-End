from fastapi import APIRouter, HTTPException, status, Depends
from charlie.applications.owners.schemas import OwnerIn, OwnerOut
from charlie.dependencies.database import get_database
from bson import ObjectId
import os
import json
from charlie.applications.owners.controllers import OwnerController

router = APIRouter(prefix="/owners", tags=["owners"])
OWNER_DB_PATH = os.path.join("db", "owners.json")

def load_owners():
    if not os.path.exists(OWNER_DB_PATH):
        with open(OWNER_DB_PATH, "w") as f:
            json.dump({}, f)
        return {}
    with open(OWNER_DB_PATH, "r") as f:
        return json.load(f)

# Use Depends para injetar o banco de dados
def get_owner_controller(db=Depends(get_database)):
    return OwnerController(db)

# Endpoint para criar um novo proprietário
@router.post("/owners", response_model=OwnerOut, status_code=status.HTTP_201_CREATED)
async def create_owner(owner: OwnerIn, owner_controller=Depends(get_owner_controller)):
    return await owner_controller.create_one(owner)

# Endpoint para obter um proprietário por ID
@router.get("/owners/{owner_id}", response_model=OwnerOut)
async def get_owner(owner_id: str, db=Depends(get_database)):
    try:
        oid = ObjectId(owner_id)
    except Exception:
        raise HTTPException(status_code=400, detail="ID de proprietário inválido")
    
    owner = await db.owners.find_one({"_id": oid})
    if not owner:
        raise HTTPException(status_code=404, detail="Proprietário não encontrado")
    return owner

# Endpoint para atualizar um proprietário
@router.put("/owners/{owner_id}", response_model=OwnerOut)
async def update_owner(owner_id: str, owner_update: OwnerIn, db=Depends(get_database)):
    try:
        oid = ObjectId(owner_id)
    except Exception:
        raise HTTPException(status_code=400, detail="ID de proprietário inválido")
    
    update_data = {k: v for k, v in owner_update.dict().items() if v is not None}
    result = await db.owners.update_one({"_id": oid}, {"$set": update_data})
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Proprietário não encontrado ou não modificado")
    
    updated_owner = await db.owners.find_one({"_id": oid})
    return updated_owner

# Endpoint para deletar um proprietário
@router.delete("/owners/{owner_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_owner(owner_id: str, db=Depends(get_database)):
    try:
        oid = ObjectId(owner_id)
    except Exception:
        raise HTTPException(status_code=400, detail="ID de proprietário inválido")
    
    result = await db.owners.delete_one({"_id": oid})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Proprietário não encontrado")
