from fastapi import APIRouter, Depends, HTTPException, status, Query
from pytest import skip
from sqlalchemy.orm import Session

from app.database import get_db

from app.models import AvaliacaoPedido, ItemPedido
from app.schema.avaliacao_pedido_schema import AvaliacaoPedidoCreate, AvaliacaoPedidoUpdate, AvaliacaoPedidoRead
from app.schema.pagination_schema import PaginatedResponse, calculate_pagination

from app.service.utils import generate_id, calcular_media_avaliacoes, calcular_media_avaliacoes_produto
from app.models.pedido import Pedido

route = APIRouter(prefix="/avaliacao_pedidos", tags=["avaliacao_pedidos"])

def recalcular_medias_produtos(db: Session, id_pedido: str):
    """Recalcula as médias de avaliação dos produtos que estão neste pedido"""
    items = db.query(ItemPedido).filter(ItemPedido.id_pedido == id_pedido).all()
    for item in items:
        calcular_media_avaliacoes_produto(db, item.id_produto)

@route.post('/', response_model=AvaliacaoPedidoRead, status_code=status.HTTP_201_CREATED)
def create_avaliacao_pedido(body: AvaliacaoPedidoCreate, db: Session = Depends(get_db)):
    _avaliacao_pedido_id = generate_id()

    pedido = db.query(Pedido).filter(Pedido.id_pedido == body.id_pedido).first()

    if not pedido:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pedido avaliado não existe")

    if not body.titulo_comentario:
        body.titulo_comentario = 'Sem Titulo'

    if not body.comentario:
        body.comentario = 'Sem Comentário'

    db_avaliacao_pedido = AvaliacaoPedido(
        id_avaliacao=_avaliacao_pedido_id,
        id_pedido=body.id_pedido,
        avaliacao=body.avaliacao,
        titulo_comentario=body.titulo_comentario,
        comentario=body.comentario
    )

    db.add(db_avaliacao_pedido)
    db.commit()
    db.refresh(db_avaliacao_pedido)
    
    # Recalcula a média de avaliações do pedido
    calcular_media_avaliacoes(db, body.id_pedido)
    
    # Recalcula as médias de avaliações dos produtos
    recalcular_medias_produtos(db, body.id_pedido)
    
    return db_avaliacao_pedido

@route.get('/', response_model=PaginatedResponse[AvaliacaoPedidoRead])
def read_avaliacao_pedidos(
    skip: int = Query(0, ge=0, description="Items a pular"),
    limit: int = Query(10, ge=1, le=100, description="Items por página"),
    db: Session = Depends(get_db)
):
    total = db.query(AvaliacaoPedido).count()
    avaliacao_pedidos = db.query(AvaliacaoPedido).offset(skip).limit(limit).all()
    pagination_info = calculate_pagination(total, skip, limit)
    return PaginatedResponse(
        data=avaliacao_pedidos,
        **pagination_info
    )

@route.get('/{id_avaliacao}', response_model=AvaliacaoPedidoRead)
def read_avaliacao_pedido(id_avaliacao: str, db: Session = Depends(get_db)):
    avaliacao_pedido = db.query(AvaliacaoPedido).filter(AvaliacaoPedido.id_avaliacao == id_avaliacao).first()
    if not avaliacao_pedido:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Avaliação do pedido não encontrada")
    return avaliacao_pedido

@route.patch('/{id_avaliacao}', response_model=AvaliacaoPedidoRead)
def update_avaliacao_pedido(id_avaliacao: str, body: AvaliacaoPedidoUpdate, db: Session = Depends(get_db)):
    avaliacao_pedido = db.query(AvaliacaoPedido).filter(AvaliacaoPedido.id_avaliacao == id_avaliacao).first()


    if not avaliacao_pedido:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Avaliação do pedido não encontrada")

    pedido = db.query(Pedido).filter(Pedido.id_pedido == avaliacao_pedido.id_pedido).first()

    if not pedido:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pedido avaliado não existe")

    for key, value in body.model_dump(exclude_unset=True).items():
        setattr(avaliacao_pedido, key, value)

    db.commit()
    db.refresh(avaliacao_pedido)

    if body.avaliacao is not None:    
        calcular_media_avaliacoes(db, avaliacao_pedido.id_pedido)
        # Recalcula as médias de avaliações dos produtos
        recalcular_medias_produtos(db, avaliacao_pedido.id_pedido)
    
    return avaliacao_pedido

@route.delete('/{id_avaliacao}', status_code=status.HTTP_204_NO_CONTENT)
def delete_avaliacao_pedido(id_avaliacao: str, db: Session = Depends(get_db)):
    avaliacao_pedido = db.query(AvaliacaoPedido).filter(AvaliacaoPedido.id_avaliacao == id_avaliacao).first()
    if not avaliacao_pedido:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Avaliação do pedido não encontrada")

    id_pedido = avaliacao_pedido.id_pedido
    db.delete(avaliacao_pedido)
    db.commit()
    
    # Recalcula a média de avaliações do pedido
    calcular_media_avaliacoes(db, id_pedido)
    
    # Recalcula as médias de avaliações dos produtos
    recalcular_medias_produtos(db, id_pedido)