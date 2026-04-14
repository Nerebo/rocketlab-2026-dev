from pydantic import BaseModel, Field, ConfigDict, field_serializer
from typing import Optional, Dict
from datetime import datetime

class ProdutoBase(BaseModel):
    nome_produto: str = Field(..., min_length=1, max_length=255)
    categoria_produto: str = Field(..., min_length=1, max_length=100)
    peso_produto_gramas: Optional[float] = Field(None, gt=0)
    comprimento_centimetros: Optional[float] = Field(None, gt=0)
    altura_centimetros: Optional[float] = Field(None, gt=0)
    largura_centimetros: Optional[float] = Field(None, gt=0)

class ProdutoCreate(ProdutoBase):
    pass

class ProdutoUpdate(BaseModel):
    nome_produto: Optional[str] = Field(None, min_length=1, max_length=255)
    categoria_produto: Optional[str] = Field(None, min_length=1, max_length=100)
    peso_produto_gramas: Optional[float] = Field(None, gt=0)
    comprimento_centimetros: Optional[float] = Field(None, gt=0)
    altura_centimetros: Optional[float] = Field(None, gt=0)
    largura_centimetros: Optional[float] = Field(None, gt=0)
    link_imagem: Optional[str] = Field(None, max_length=500)
    media_avaliacoes: Optional[float] = None

class ProdutoRead(ProdutoBase):
    id_produto: str
    link_imagem: Optional[str] = Field(None, max_length=500)
    media_avaliacoes: Optional[float] = None
    model_config = ConfigDict(from_attributes=True)
    categoria_produto: str = Field(..., min_length=0, max_length=100)
    peso_produto_gramas: Optional[float] = Field(None)
    

class AvaliacaoRead(BaseModel):
    """Schema for reading reviews/evaluations"""
    id_avaliacao: str
    id_pedido: str
    avaliacao: int = Field(..., ge=1, le=5)
    titulo_comentario: Optional[str] = None
    comentario: Optional[str] = None
    data_comentario: Optional[datetime] = None
    data_resposta: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)
    
    @field_serializer('data_comentario', 'data_resposta')
    def serialize_datetime(self, value: Optional[datetime]) -> Optional[str]:
        """Convert datetime to ISO format string"""
        if value is None:
            return None
        return value.isoformat() if isinstance(value, datetime) else str(value)


class MediaAvaliacaoResponse(BaseModel):
    """Schema for aggregated rating statistics"""
    id_produto: str
    media: float = Field(..., ge=0, le=5)
    total: int = Field(..., ge=0)
    breakdown: Dict[int, int] = Field(
        ..., 
        description="Count of ratings for each star level (1-5)"
    )
    
    model_config = ConfigDict(from_attributes=True)


class MediaAvaliacaoBatchRequest(BaseModel):
    """Schema for requesting batch media evaluations"""
    ids_produto: list[str] = Field(..., min_items=1, max_items=100)


class MediaAvaliacaoBatchResponse(BaseModel):
    """Schema for batch media evaluations response"""
    data: list[MediaAvaliacaoResponse]
    model_config = ConfigDict(from_attributes=True)
