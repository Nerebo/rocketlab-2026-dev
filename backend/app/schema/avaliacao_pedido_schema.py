from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

class AvaliacaoPedidoBase(BaseModel):
    id_pedido: str = Field(..., min_length=1, max_length=32)
    avaliacao: int = Field(..., ge=1, le=5)
    titulo_comentario: Optional[str] = Field(None, min_length=1, max_length=255)
    comentario: Optional[str] = Field(None, min_length=1, max_length=1000)

class AvaliacaoPedidoCreate(AvaliacaoPedidoBase):
    pass

class AvaliacaoPedidoUpdate(BaseModel):
    avaliacao: Optional[int] = Field(None, ge=1, le=5)
    titulo_comentario: Optional[str] = Field(None, min_length=1, max_length=255)
    comentario: Optional[str] = Field(None, min_length=1, max_length=1000)

class AvaliacaoPedidoRead(AvaliacaoPedidoBase):
    id_avaliacao: str
    model_config = ConfigDict(from_attributes=True)