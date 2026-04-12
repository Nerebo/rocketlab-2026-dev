from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
import datetime

class PedidoBase(BaseModel):
    id_consumidor: str = Field(..., max_length=32)
    pedido_compra_timestamp: Optional[datetime.datetime] = None

class PedidoCreate(PedidoBase):
    pass

class PedidoUpdate(PedidoBase):
    status: Optional[str] = Field(None, max_length=50)
    pedido_entregue_timestamp: Optional[datetime.datetime] = None
    data_estimada_entrega: Optional[datetime.date] = None
    tempo_entrega_dias: Optional[float] = None
    tempo_entrega_estimado_dias: Optional[float] = None
    diferenca_entrega_dias: Optional[float] = None
    entrega_no_prazo: Optional[str] = Field(None, max_length=10)

class PedidoRead(PedidoBase):
    id_pedido: str
    id_consumidor: Optional[str] = Field(None, max_length=32)
    status: Optional[str] = Field(None, max_length=50)
    pedido_entregue_timestamp: Optional[datetime.datetime] = None
    data_estimada_entrega: Optional[datetime.date] = None
    tempo_entrega_dias: Optional[float] = None
    tempo_entrega_estimado_dias: Optional[float] = None
    diferenca_entrega_dias: Optional[float] = None
    entrega_no_prazo: Optional[str] = Field(None, max_length=16)
    model_config = ConfigDict(from_attributes=True)