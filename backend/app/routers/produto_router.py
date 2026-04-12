from fastapi import APIRouter, Depends, HTTPException, status
from pytest import skip
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Produto
from app.schema.produto_schema import ProdutoCreate, ProdutoUpdate, ProdutoRead

from app.service.utils import generate_id

route = APIRouter(prefix="/produtos", tags=["produtos"])

@route.post('/', response_model=ProdutoCreate, status_code=status.HTTP_201_CREATED)
def create_produto(body: ProdutoCreate, db: Session = Depends(get_db)):
    _produto_id = generate_id()

    if db.query(Produto).filter(Produto.id_produto == body.id_produto).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Produto já existe")

    db_produto = Produto(
        id_produto=_produto_id,
        nome_produto=body.nome_produto,
        descricao=body.descricao,
        preco_BRL=body.preco_BRL,
        peso_kg=body.peso_kg,
        categoria=body.categoria
    )

    db.add(db_produto)
    db.commit()
    db.refresh(db_produto)
    return db_produto

@route.get('/', response_model=list[ProdutoRead])
def read_produtos(db: Session = Depends(get_db)):
    produtos = db.query(Produto).all()
    return produtos

@route.get('/{nome}', response_model=list[ProdutoRead])
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