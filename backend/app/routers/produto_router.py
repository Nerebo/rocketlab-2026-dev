from fastapi import APIRouter, Depends, HTTPException, status, Query
from pytest import skip
from sqlalchemy.orm import Session
from sqlalchemy import func, desc, case
from typing import Optional

from app.database import get_db
from app.models import Produto, ItemPedido, AvaliacaoPedido
from app.schema.produto_schema import (
    ProdutoCreate, ProdutoUpdate, ProdutoRead,
    AvaliacaoRead, MediaAvaliacaoResponse, 
    MediaAvaliacaoBatchRequest, MediaAvaliacaoBatchResponse
)
from app.schema.pagination_schema import PaginatedResponse, calculate_pagination

from app.service.utils import generate_id

route = APIRouter(prefix="/produtos", tags=["produtos"])

@route.post('/', response_model=ProdutoRead, status_code=status.HTTP_201_CREATED)
def create_produto(body: ProdutoCreate, db: Session = Depends(get_db)):
    _produto_id = generate_id()

    db_produto = Produto(
        id_produto=_produto_id,
        nome_produto=body.nome_produto,
        peso_produto_gramas=body.peso_produto_gramas,
        comprimento_centimetros=body.comprimento_centimetros,
        altura_centimetros=body.altura_centimetros,
        largura_centimetros=body.largura_centimetros,
        categoria_produto=body.categoria_produto
    )

    db.add(db_produto)
    db.commit()
    db.refresh(db_produto)
    return db_produto

@route.get('/', response_model=PaginatedResponse[ProdutoRead])
def read_produtos(
    skip: int = Query(0, ge=0, description="Items a pular"),
    limit: int = Query(10, ge=1, le=100, description="Items por página"),
    db: Session = Depends(get_db)
    ):
    total = db.query(Produto).count()
    produtos = db.query(Produto).offset(skip).limit(limit).all()
    pagination_info = calculate_pagination(total, skip, limit)
    return PaginatedResponse(
        data=produtos,
        **pagination_info
    )

# Specific routes BEFORE generic /{id_produto} route
@route.get('/buscar/{nome}', response_model=PaginatedResponse[ProdutoRead])
def read_produto(
    nome: str,
    skip: int = Query(0, ge=0, description="Items a pular"),
    limit: int = Query(12, ge=1, le=100, description="Items por página"),
    db: Session = Depends(get_db)
):
    """Busca produtos por nome com paginação (máximo 100 resultados)"""
    # Primeiro, contar todos os produtos que correspondem (até 100)
    query = db.query(Produto).filter(Produto.nome_produto.ilike(f"%{nome}%")).limit(100)
    total = query.count()
    
    # Aplicar paginação
    produtos = query.offset(skip).limit(limit).all()
    
    if not produtos and skip == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produto não encontrado")
    
    # Usar o total (máximo 100) para cálculo de paginação
    actual_total = min(total, 100)
    pagination_info = calculate_pagination(actual_total, skip, limit)
    
    return PaginatedResponse(
        data=produtos,
        **pagination_info
    )

@route.post('/media-avaliacao/batch', response_model=MediaAvaliacaoBatchResponse)
def get_produtos_media_avaliacao_batch(body: MediaAvaliacaoBatchRequest, db: Session = Depends(get_db)):
    """
    Get aggregated rating statistics for multiple products in a single request.
    This endpoint prevents N+1 queries when loading multiple product ratings.
    """
    resultados = []
    
    for id_produto in body.ids_produto:
        # Verify produto exists
        produto = db.query(Produto).filter(Produto.id_produto == id_produto).first()
        if not produto:
            # Skip products that don't exist
            continue
        
        # Single optimized query with breakdown
        result = (
            db.query(
                func.avg(AvaliacaoPedido.avaliacao).label("media"),
                func.count(AvaliacaoPedido.id_avaliacao).label("total"),
                func.sum(case((AvaliacaoPedido.avaliacao == 1, 1), else_=0)).label("count_1"),
                func.sum(case((AvaliacaoPedido.avaliacao == 2, 1), else_=0)).label("count_2"),
                func.sum(case((AvaliacaoPedido.avaliacao == 3, 1), else_=0)).label("count_3"),
                func.sum(case((AvaliacaoPedido.avaliacao == 4, 1), else_=0)).label("count_4"),
                func.sum(case((AvaliacaoPedido.avaliacao == 5, 1), else_=0)).label("count_5"),
            )
            .join(
                ItemPedido,
                ItemPedido.id_pedido == AvaliacaoPedido.id_pedido
            )
            .filter(ItemPedido.id_produto == id_produto)
            .filter(AvaliacaoPedido.avaliacao.isnot(None))
            .first()
        )
        
        media = round(float(result[0]) if result[0] else 0, 2)
        total = result[1] if result[1] else 0
        
        # Build breakdown dictionary
        breakdown = {
            1: result[2] or 0,
            2: result[3] or 0,
            3: result[4] or 0,
            4: result[5] or 0,
            5: result[6] or 0,
        }
        
        resultados.append(MediaAvaliacaoResponse(
            media=media,
            total=total,
            breakdown=breakdown,
            id_produto=id_produto
        ))
    
    return MediaAvaliacaoBatchResponse(data=resultados)

@route.get('/{id_produto}/avaliacoes', response_model=list[AvaliacaoRead])
def get_produto_avaliacoes(id_produto: str, db: Session = Depends(get_db)):
    """
    Get all reviews for a specific product.
    Aggregates reviews from all orders containing this product.
    """
    try:
        # Verify produto exists
        produto = db.query(Produto).filter(Produto.id_produto == id_produto).first()
        if not produto:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Produto não encontrado"
            )
        
        # Get item_pedidos for this product
        item_pedido_ids = db.query(ItemPedido.id_pedido).filter(
            ItemPedido.id_produto == id_produto
        ).distinct().all()
        
        if not item_pedido_ids:
            return []
        
        pedido_ids = [ip[0] for ip in item_pedido_ids]
        
        # Get avaliacoes for these pedidos
        avaliacoes = (
            db.query(AvaliacaoPedido)
            .filter(AvaliacaoPedido.id_pedido.in_(pedido_ids))
            .filter(AvaliacaoPedido.avaliacao.isnot(None))
            .order_by(desc(AvaliacaoPedido.data_comentario))
            .all()
        )
        
        return avaliacoes if avaliacoes else []
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        print(f"Erro na rota de avaliacoes: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao buscar avaliações: {str(e)}"
        )

@route.get('/{id_produto}/media-avaliacao', response_model=MediaAvaliacaoResponse)
def get_produto_media_avaliacao(id_produto: str, db: Session = Depends(get_db)):
    """
    Get aggregated rating statistics for a product.
    Returns average rating, count, and breakdown by rating level.
    """
    try:
        # Verify produto exists
        produto = db.query(Produto).filter(Produto.id_produto == id_produto).first()
        if not produto:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Produto não encontrado"
            )
        
        # Get item_pedidos for this product
        item_pedido_ids = db.query(ItemPedido.id_pedido).filter(
            ItemPedido.id_produto == id_produto
        ).distinct().all()
        
        if not item_pedido_ids:
            return MediaAvaliacaoResponse(
                id_produto=id_produto,
                media=0.0,
                total=0,
                breakdown={1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
            )
        
        pedido_ids = [ip[0] for ip in item_pedido_ids]
        
        # Get ratings for these pedidos
        result = (
            db.query(
                func.avg(AvaliacaoPedido.avaliacao).label("media"),
                func.count(AvaliacaoPedido.id_avaliacao).label("total"),
                func.sum(case((AvaliacaoPedido.avaliacao == 1, 1), else_=0)).label("count_1"),
                func.sum(case((AvaliacaoPedido.avaliacao == 2, 1), else_=0)).label("count_2"),
                func.sum(case((AvaliacaoPedido.avaliacao == 3, 1), else_=0)).label("count_3"),
                func.sum(case((AvaliacaoPedido.avaliacao == 4, 1), else_=0)).label("count_4"),
                func.sum(case((AvaliacaoPedido.avaliacao == 5, 1), else_=0)).label("count_5"),
            )
            .filter(AvaliacaoPedido.id_pedido.in_(pedido_ids))
            .filter(AvaliacaoPedido.avaliacao.isnot(None))
            .first()
        )
        
        if not result or result[1] == 0:
            return MediaAvaliacaoResponse(
                id_produto=id_produto,
                media=0.0,
                total=0,
                breakdown={1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
            )
        
        media = round(float(result[0]) if result[0] else 0, 2)
        total = int(result[1]) if result[1] else 0
        
        # Build breakdown dictionary
        breakdown = {
            1: int(result[2] or 0),
            2: int(result[3] or 0),
            3: int(result[4] or 0),
            4: int(result[5] or 0),
            5: int(result[6] or 0),
        }
        
        return MediaAvaliacaoResponse(
            media=media,
            total=total,
            breakdown=breakdown,
            id_produto=id_produto
        )
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        print(f"Erro na rota de media-avaliacao: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao buscar média de avaliações: {str(e)}"
        )

# Generic routes AFTER specific ones
@route.get('/{id_produto}', response_model=ProdutoRead)
def read_produto_by_id(id_produto: str, db: Session = Depends(get_db)):
    produto = db.query(Produto).filter(Produto.id_produto == id_produto).first()
    if not produto:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produto não encontrado")
    return produto

@route.patch('/{id_produto}', response_model=ProdutoRead)
def update_produto(id_produto: str, body: ProdutoUpdate, db: Session = Depends(get_db)):
    produto = db.query(Produto).filter(Produto.id_produto == id_produto).first()
    if not produto:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produto não encontrado")

    for key, value in body.model_dump(exclude_unset=True).items():
        setattr(produto, key, value)

    db.commit()
    db.refresh(produto)
    return produto

@route.delete('/{id_produto}', status_code=status.HTTP_204_NO_CONTENT)
def delete_produto(id_produto: str, db: Session = Depends(get_db)):
    produto = db.query(Produto).filter(Produto.id_produto == id_produto).first()
    if not produto:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produto não encontrado")

    db.delete(produto)
    db.commit()
    return None