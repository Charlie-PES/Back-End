from datetime import date
from pydantic import BaseModel, Field
from typing import Optional, List

# Classe de Visitas
class Visita(BaseModel):
    id: str  # Usando string como ID
    data_visita: date = Field(default_factory=date.today)  # Data da visita
    tipo: str  # Tipo da visita (ex: acompanhamento, inspeção)
    observacoes: str  # Observações sobre a visita


# Schema para entrada (registro de nova adoção)
class AdoptionIn(BaseModel):
    pet_id: str  # Usando string como ID
    adopter_id: str  # Usando string como ID
    adoption_date: date = Field(default_factory=date.today)
    acompanhamento_ativo: bool = True
    visitas: Optional[List[Visita]] = []  # Lista de visitas realizadas


# Schema para saída (detalhes da adoção)
class AdoptionOut(BaseModel):
    id: str 
    pet_id: str  # Usando string como ID
    pet_name: str
    adopter_id: str  # Usando string como ID
    adopter_name: str
    adoption_date: date
    acompanhamento_ativo: bool
    visitas: List[Visita] = []  # Adicionando a lista de visitas

    class Config:
        arbitrary_types_allowed = True
        from_attributes = True

# Schema para atualização (atualização do status do acompanhamento)
class AdoptionUpdate(BaseModel):
    acompanhamento_ativo: Optional[bool]
    visitas: Optional[List[Visita]]  # Adiciona a possibilidade de atualizar as visitas
