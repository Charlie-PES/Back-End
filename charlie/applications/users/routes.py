import os
import json
import bcrypt
from fastapi import APIRouter, HTTPException, status
from typing import List
from pydantic import BaseModel

from .schemas import Item, ItemCreate, UserCreate

router = APIRouter(prefix="/users", tags=["users"])

# Definindo os caminhos dos arquivos JSON
USERS_DB_PATH = os.path.join("db", "users.json")
ITEMS_DB_PATH = os.path.join("db", "items.json")

# Funções para hash de senha
def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

# Funções auxiliares para carregar e salvar os dados
def load_db(file_path: str):
    if not os.path.exists(file_path):
        with open(file_path, "w") as f:
            json.dump({}, f)
        return {}
    with open(file_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            data = {}
    return data


def save_db(file_path: str, data):
    with open(file_path, "w") as f:
        json.dump(data, f)


def load_users():
    return load_db(USERS_DB_PATH)


def save_users(data):
    save_db(USERS_DB_PATH, data)


def load_items():
    return load_db(ITEMS_DB_PATH)


def save_items(data):
    save_db(ITEMS_DB_PATH, data)


# Endpoint de teste
@router.get("/test")
async def test():
    return {"message": "This is a test for the router"}


# Endpoints de autenticação
@router.post("/auth/register", status_code=status.HTTP_201_CREATED)
async def register(user: UserCreate):
    users_db = load_users()
    # Verifica se já existe usuário com o mesmo username ou email
    for existing_user in users_db.values():
        if (
            existing_user.get("username") == user.username
            or existing_user.get("email") == user.email
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists"
            )

    new_id = max([int(i) for i in users_db.keys()], default=0) + 1 if users_db else 1

    # Cria o dicionário do usuário com a senha hasheada
    new_user_dict = {
        "id": new_id,
        "username": user.username,
        "email": user.email,
        "password": hash_password(user.password),
    }
    users_db[str(new_id)] = new_user_dict
    save_users(users_db)
    return {"message": "User registered successfully", "user": new_user_dict}


# Modelo para dados de login
class LoginRequest(BaseModel):
    username: str
    password: str

@router.post("/auth/login")
async def login(login_data: LoginRequest):
    users_db = load_users()  # Carrega os usuários do banco de dados
    for user_data in users_db.values():
        if user_data["username"] == login_data.username:
            # Verifica a senha usando bcrypt
            if not verify_password(login_data.password, user_data.get("password")):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid credentials",
                )
            user_data.pop("password", None)  # Remover a senha antes de retornar
            return {"message": "Login successful", "user": user_data}
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
    )


@router.get("/auth/profile")
async def profile(user_id: int):
    users_db = load_users()
    user_data = users_db.get(str(user_id))
    if user_data:
        user_data.pop("password", None)
        return user_data
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")


# Endpoints CRUD para itens
@router.get("/items", response_model=List[Item])
async def get_items():
    items_db = load_items()
    return [Item(**item) for item in items_db.values()]


@router.get("/items/{item_id}", response_model=Item)
async def get_item(item_id: int):
    items_db = load_items()
    item_data = items_db.get(str(item_id))
    if item_data:
        return Item(**item_data)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")


@router.post("/items", response_model=Item, status_code=status.HTTP_201_CREATED)
async def create_item(item: ItemCreate):
    items_db = load_items()

    # Verifica se já existe um item com o mesmo nome
    for existing_item in items_db.values():
        if existing_item.get("name") == item.name:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Item already exists"
            )

    new_id = max([int(i) for i in items_db.keys()], default=0) + 1 if items_db else 1
    new_item = Item(id=new_id, name=item.name, description=item.description)
    items_db[str(new_id)] = new_item.dict()
    save_items(items_db)
    return new_item


@router.put("/items/{item_id}", response_model=Item)
async def update_item(item_id: int, item: ItemCreate):
    items_db = load_items()
    if str(item_id) not in items_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
        )
    updated_item = Item(id=item_id, name=item.name, description=item.description)
    items_db[str(item_id)] = updated_item.dict()
    save_items(items_db)
    return updated_item


@router.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(item_id: int):
    items_db = load_items()
    if str(item_id) in items_db:
        del items_db[str(item_id)]
        save_items(items_db)
        return
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
