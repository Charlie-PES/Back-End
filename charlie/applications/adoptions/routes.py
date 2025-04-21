from fastapi import APIRouter, HTTPException, status, Depends
from charlie.applications.adoptions.schemas import AdoptionIn, AdoptionOut, AdoptionUpdate, Visita
from charlie.settings import Settings
from bson import ObjectId
from typing import List
import os
import json
from charlie.dependencies.database import get_database

router = APIRouter(prefix="/adoptions", tags=["adoptions"])
ADOPTIONS_DB_PATH = os.path.join("db", "adoptions.json")

# Função auxiliar para obter nomes de pet e adotante
async def get_pet_and_adopter_names(db, pet_id: str, adopter_id: str):
    pet = await db.pets.find_one({"_id": ObjectId(pet_id)})
    adopter = await db.owners.find_one({"_id": ObjectId(adopter_id)})
    return pet.get("name", "Unknown"), adopter.get("name", "Unknown")

# Endpoint para criar uma nova adoção
@router.post("/adoptions", response_model=AdoptionOut, status_code=status.HTTP_201_CREATED)
async def create_adoption(adoption: AdoptionIn, db=Depends(get_database)):
    pet_name, adopter_name = await get_pet_and_adopter_names(db, adoption.pet_id, adoption.adopter_id)
    adoption_data = adoption.dict()
    adoption_data["pet_name"] = pet_name
    adoption_data["adopter_name"] = adopter_name
    result = await db.adoptions.insert_one(adoption_data)
    adoption_data["id"] = str(result.inserted_id)
    return adoption_data

# Endpoint para obter uma adoção por ID
@router.get("/adoptions/{adoption_id}", response_model=AdoptionOut)
async def get_adoption(adoption_id: str, db=Depends(get_database)):
    try:
        oid = ObjectId(adoption_id)
    except Exception:
        raise HTTPException(status_code=400, detail="ID de adoção inválido")
    adoption = await db.adoptions.find_one({"_id": oid})
    if not adoption:
        raise HTTPException(status_code=404, detail="Adoção não encontrada")
    return adoption

# Endpoint para atualizar uma adoção
@router.put("/adoptions/{adoption_id}", response_model=AdoptionOut)
async def update_adoption(adoption_id: str, adoption_update: AdoptionUpdate, db=Depends(get_database)):
    try:
        oid = ObjectId(adoption_id)
    except Exception:
        raise HTTPException(status_code=400, detail="ID de adoção inválido")
    update_data = {k: v for k, v in adoption_update.dict().items() if v is not None}
    result = await db.adoptions.update_one({"_id": oid}, {"$set": update_data})
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Adoção não encontrada ou não modificada")
    updated_adoption = await db.adoptions.find_one({"_id": oid})
    return updated_adoption

# Endpoint para adicionar uma visita a uma adoção
@router.post("/adoptions/{adoption_id}/visitas", response_model=Visita, status_code=status.HTTP_201_CREATED)
async def add_visit(adoption_id: str, visita: Visita, db=Depends(get_database)):
    try:
        oid = ObjectId(adoption_id)
    except Exception:
        raise HTTPException(status_code=400, detail="ID de adoção inválido")
    visit_id = str(ObjectId())
    visita_data = visita.dict()
    visita_data["id"] = visit_id
    result = await db.adoptions.update_one({"_id": oid}, {"$push": {"visitas": visita_data}})
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Adoção não encontrada")
    return visita_data

# Endpoint para obter uma visita por ID
@router.get("/adoptions/{adoption_id}/visitas/{visit_id}", response_model=Visita)
async def get_visit(adoption_id: str, visit_id: str, db=Depends(get_database)):
    try:
        oid = ObjectId(adoption_id)
    except Exception:
        raise HTTPException(status_code=400, detail="ID de adoção inválido")
    adoption = await db.adoptions.find_one({"_id": oid, "visitas.id": visit_id}, {"visitas.$": 1})
    if not adoption or not adoption.get("visitas"):
        raise HTTPException(status_code=404, detail="Visita não encontrada")
    return adoption["visitas"][0]

# Endpoint para atualizar uma visita
@router.put("/adoptions/{adoption_id}/visitas/{visit_id}", response_model=Visita)
async def update_visit(adoption_id: str, visit_id: str, visita_update: Visita, db=Depends(get_database)):
    try:
        oid = ObjectId(adoption_id)
    except Exception:
        raise HTTPException(status_code=400, detail="ID de adoção inválido")
    update_data = {f"visitas.$.{k}": v for k, v in visita_update.dict().items() if v is not None}
    result = await db.adoptions.update_one({"_id": oid, "visitas.id": visit_id}, {"$set": update_data})
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Visita não encontrada ou não modificada")
    updated_adoption = await db.adoptions.find_one({"_id": oid, "visitas.id": visit_id}, {"visitas.$": 1})
    return updated_adoption["visitas"][0]
