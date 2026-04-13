from sqlite3 import IntegrityError

from fastapi import APIRouter, Depends, HTTPException, status, Query
from pytest import skip
from sqlalchemy.orm import Session

from app.database import get_db

from app.models import Pedido, AvaliacaoPedido
from app.schema.pedido_schema import PedidoCreate, PedidoUpdate, PedidoRead
from app.schema.pagination_schema import PaginatedResponse, calculate_pagination

from app.service.utils import generate_id
from datetime import datetime, date

from app.models.consumidor import Consumidor

status_permitidos = set(['entregue', 'faturado', 'enviado', 'em processamento', 'indisponível', 'cancelado', 'criado', 'aprovado'])

route = APIRouter(prefix="/pedidos", tags=["pedidos"])
@route.post('/', response_model=PedidoRead, status_code=status.HTTP_201_CREATED)
def create_pedido(body: PedidoCreate, db: Session = Depends(get_db)):
    _pedido_id = generate_id()

    db_pedido = db.query(Pedido).filter(Pedido.id_pedido == _pedido_id).first()

    db_consumidor = db.query(Consumidor).filter(Consumidor.id_consumidor == body.id_consumidor).first()

    if not db_consumidor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Consumidor não encontrado")

    db_pedido = Pedido(
        id_pedido=_pedido_id,
        id_consumidor=body.id_consumidor,
        status='criado',  # TODO: Adicionar função para adicionar as datas a medida que o pedido for evoluindo
        pedido_compra_timestamp=datetime.now() 
    )

    db.add(db_pedido)
    db.commit()
    db.refresh(db_pedido)
    return db_pedido

@route.get('/', response_model=PaginatedResponse[PedidoRead])
def read_pedidos(
    skip: int = Query(0, ge=0, description="Items a pular"),
    limit: int = Query(10, ge=1, le=100, description="Items por página"),
    db: Session = Depends(get_db)
):
    total = db.query(Pedido).count()
    pedidos = db.query(Pedido).offset(skip).limit(limit).all()
    pagination_info = calculate_pagination(total, skip, limit)
    return PaginatedResponse(
        data=pedidos,
        **pagination_info
    )

@route.get('/{id_pedido}', response_model=PedidoRead)
def read_pedido(id_pedido: str, db: Session = Depends(get_db)):
    pedido = db.query(Pedido).filter(Pedido.id_pedido == id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pedido não encontrado")
    return pedido

@route.patch('/{id_pedido}', response_model=PedidoRead)
def update_pedido(id_pedido: str, body: PedidoUpdate, db: Session = Depends(get_db)):
    pedido = db.query(Pedido).filter(Pedido.id_pedido == id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pedido não encontrado")

    if body.status and body.status not in status_permitidos:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Status inválido. Status permitidos: {', '.join(status_permitidos)}")
    
    for key, value in body.model_dump(exclude_unset=True).items():
        setattr(pedido, key, value)

    db.commit()
    db.refresh(pedido)
    return pedido

@route.delete('/{id_pedido}', status_code=status.HTTP_204_NO_CONTENT)
def delete_pedido(id_pedido: str, db: Session = Depends(get_db)):
    pedido = db.query(Pedido).filter(Pedido.id_pedido == id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pedido não encontrado")

    avaliacoes = db.query(AvaliacaoPedido).filter(AvaliacaoPedido.id_pedido == id_pedido).all()
    if avaliacoes:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Não é possível deletar um pedido que possui avaliações associadas")

    db.delete(pedido)
    db.commit()
    return None