from pydantic import BaseModel, Field
from typing import Generic, TypeVar, List, Optional

T = TypeVar('T')

class PaginationParams(BaseModel):
    """Parâmetros de paginação para requisições"""
    skip: int = Field(0, ge=0, description="Número de items a pular")
    limit: int = Field(10, ge=1, le=100, description="Número máximo de items por página (máx: 100)")

class PaginatedResponse(BaseModel, Generic[T]):
    """Resposta padronizada com paginação"""
    data: List[T]
    total: int = Field(..., description="Total de registros disponíveis")
    skip: int = Field(..., description="Items pulados")
    limit: int = Field(..., description="Items por página")
    page: int = Field(..., description="Página atual (baseado em skip/limit)")
    pages: int = Field(..., description="Total de páginas")
    
    class Config:
        json_schema_extra = {
            "example": {
                "data": [],
                "total": 100,
                "skip": 0,
                "limit": 10,
                "page": 1,
                "pages": 10
            }
        }

def calculate_pagination(total: int, skip: int, limit: int) -> dict:
    """Calcula informações de paginação"""
    page = (skip // limit) + 1 if limit > 0 else 1
    pages = (total + limit - 1) // limit if limit > 0 else 1
    
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "page": page,
        "pages": pages
    }
