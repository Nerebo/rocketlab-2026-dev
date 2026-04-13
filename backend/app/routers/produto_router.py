from fastapi import APIRouter, Depends, HTTPException, status, Query
from pytest import skip
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Produto
from app.schema.produto_schema import ProdutoCreate, ProdutoUpdate, ProdutoRead
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

@route.get('/{id_produto}', response_model=ProdutoRead)
def read_produto_by_id(id_produto: str, db: Session = Depends(get_db)):
    produto = db.query(Produto).filter(Produto.id_produto == id_produto).first()
    if not produto:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produto não encontrado")
    return produto

@route.get('/buscar/{nome}', response_model=list[ProdutoRead])
def read_produto(nome: str, db: Session = Depends(get_db)):
    produto = db.query(Produto).filter(Produto.nome_produto.ilike(f"%{nome}%")).all()
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