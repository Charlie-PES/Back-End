from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional, List
import re

# Função para validar telefone
def telefone_valido(telefone: str) -> bool:
    telefone_pattern = re.compile(r'^\(?\d{2}\)?\s?\d{4,5}-\d{4}$')
    return bool(telefone_pattern.match(telefone))

# Schema base para os dados do owner (dono)
class OwnerBase(BaseModel):
    nome_completo: str = Field(..., min_length=1)
    cpf: str = Field(..., min_length=11, max_length=14, description="CPF com ou sem pontuação")
    email: EmailStr
    telefone: Optional[str] = None
    descricao: str = Field(..., min_length=10, description="Descrição sobre o responsável")
    forma_de_resgate: Optional[str] = Field(None, description="Como os animais são resgatados/recebidos")
    localizacao: Optional[str] = Field(None, description="Local onde o responsável atua ou abriga os pets")

    # Validação do email para garantir que esteja em minúsculas
    @field_validator('email')
    def email_must_be_lower(cls, v):
        return v.lower()

    # Validação do CPF
    @field_validator('cpf')
    def cpf_valido(cls, v):
        cpf_pattern = re.compile(r'^\d{11}$|^\d{3}\.\d{3}\.\d{3}-\d{2}$')
        if not cpf_pattern.match(v):
            raise ValueError("CPF deve estar no formato 'XXXXXXXXXXX' ou 'XXX.XXX.XXX-XX'")
        return v

    # Validação do telefone
    @field_validator('telefone')
    def telefone_valido(cls, v):
        if v and not telefone_valido(v):
            raise ValueError("Telefone deve estar no formato '(XX) XXXX-XXXX' ou '(XX) XXXXX-XXXX'")
        return v

# Schema para criação de owner
class OwnerIn(OwnerBase):
    pets: List[str] = []  # Lista de IDs dos pets sob a responsabilidade do owner

# Schema para exibição do owner (saída)
class OwnerOut(OwnerBase):
    id: str  # Aqui você pode usar string se o ID for um ObjectId
    pets: List[str] = []  # Lista de pets associados ao owner

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {str: str}  # Exemplo, caso o ID seja um ObjectId no MongoDB
