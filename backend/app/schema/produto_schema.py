from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

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

class ProdutoRead(ProdutoBase):
    id_produto: str
    model_config = ConfigDict(from_attributes=True)
    categoria_produto: str = Field(..., min_length=0, max_length=100)
    peso_produto_gramas: Optional[float] = Field(None)
