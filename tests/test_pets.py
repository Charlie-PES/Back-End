import pytest
from motor.motor_asyncio import AsyncIOMotorDatabase
from charlie.applications.pets.models import PetDAO
from charlie.applications.pets.schemas import PetIn, PetTraits
from charlie.utils.pyobjectid import PyObjectId

# Mock data
mock_pet_data = {
    "name": "Luna",
    "age_months": 24,
    "traits": {
        "size": "medium",
        "breed": "Mixed",
        "color": "Brown",
        "fur_type": "medium",
        "temperament": "friendly",
        "trained": True
    },
    "picture": "https://example.com/pet-photo.jpg"
}

@pytest.mark.asyncio
async def test_create_pet(db_client: AsyncIOMotorDatabase):
    """Testa a criação de um pet no banco de dados"""
    # Criar um objeto PetIn com os dados mockados
    pet_traits = PetTraits(**mock_pet_data["traits"])
    pet_in = PetIn(
        name=mock_pet_data["name"],
        age_months=mock_pet_data["age_months"],
        traits=pet_traits,
        picture=mock_pet_data["picture"]
    )
    
    # Criar o PetDAO com um novo ObjectId
    pet_dao = PetDAO(**pet_in.model_dump(), _id=PyObjectId())
    
    # Inserir no banco de dados
    result = await db_client[pet_dao.coll_name()].insert_one(pet_dao.model_dump(by_alias=True))
    
    # Verificar se foi inserido com sucesso
    assert result.inserted_id is not None
    
    # Buscar o pet inserido
    pet_from_db = await db_client[pet_dao.coll_name()].find_one({"_id": result.inserted_id})
    
    # Verificar se os dados estão corretos
    assert pet_from_db is not None
    assert pet_from_db["name"] == mock_pet_data["name"]
    assert pet_from_db["age_months"] == mock_pet_data["age_months"]
    assert pet_from_db["traits"]["size"] == mock_pet_data["traits"]["size"]
    
    # Limpar o banco após o teste
    await db_client[pet_dao.coll_name()].delete_one({"_id": result.inserted_id})

@pytest.mark.asyncio
async def test_read_pet(db_client: AsyncIOMotorDatabase):
    """Testa a leitura de um pet do banco de dados"""
    # Primeiro criar um pet para teste
    pet_traits = PetTraits(**mock_pet_data["traits"])
    pet_in = PetIn(**mock_pet_data)
    pet_dao = PetDAO(**pet_in.model_dump(), _id=PyObjectId())
    
    # Inserir no banco
    result = await db_client[pet_dao.coll_name()].insert_one(pet_dao.model_dump(by_alias=True))
    
    # Buscar o pet
    pet_from_db = await db_client[pet_dao.coll_name()].find_one({"_id": result.inserted_id})
    
    # Verificar se encontrou e se os dados estão corretos
    assert pet_from_db is not None
    assert pet_from_db["name"] == mock_pet_data["name"]
    
    # Limpar o banco após o teste
    await db_client[pet_dao.coll_name()].delete_one({"_id": result.inserted_id})

@pytest.mark.asyncio
async def test_update_pet(db_client: AsyncIOMotorDatabase):
    """Testa a atualização de um pet no banco de dados"""
    # Primeiro criar um pet para teste
    pet_traits = PetTraits(**mock_pet_data["traits"])
    pet_in = PetIn(**mock_pet_data)
    pet_dao = PetDAO(**pet_in.model_dump(), _id=PyObjectId())
    
    # Inserir no banco
    result = await db_client[pet_dao.coll_name()].insert_one(pet_dao.model_dump(by_alias=True))
    
    # Atualizar o nome do pet
    new_name = "Max"
    update_result = await db_client[pet_dao.coll_name()].update_one(
        {"_id": result.inserted_id},
        {"$set": {"name": new_name}}
    )
    
    # Verificar se atualizou
    assert update_result.modified_count == 1
    
    # Buscar o pet atualizado
    updated_pet = await db_client[pet_dao.coll_name()].find_one({"_id": result.inserted_id})
    assert updated_pet["name"] == new_name
    
    # Limpar o banco após o teste
    await db_client[pet_dao.coll_name()].delete_one({"_id": result.inserted_id})

@pytest.mark.asyncio
async def test_delete_pet(db_client: AsyncIOMotorDatabase):
    """Testa a deleção de um pet do banco de dados"""
    # Primeiro criar um pet para teste
    pet_traits = PetTraits(**mock_pet_data["traits"])
    pet_in = PetIn(**mock_pet_data)
    pet_dao = PetDAO(**pet_in.model_dump(), _id=PyObjectId())
    
    # Inserir no banco
    result = await db_client[pet_dao.coll_name()].insert_one(pet_dao.model_dump(by_alias=True))
    
    # Deletar o pet
    delete_result = await db_client[pet_dao.coll_name()].delete_one({"_id": result.inserted_id})
    
    # Verificar se deletou
    assert delete_result.deleted_count == 1
    
    # Tentar buscar o pet deletado
    deleted_pet = await db_client[pet_dao.coll_name()].find_one({"_id": result.inserted_id})
    assert deleted_pet is None
