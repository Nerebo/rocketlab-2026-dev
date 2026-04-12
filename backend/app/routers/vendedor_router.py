from fastapi import APIRouter, Depends, HTTPException, status
from pytest import skip
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Vendedor
from app.schema.vendedor_schema import VendedorCreate, VendedorUpdate, VendedorRead

from app.service.utils import generate_id

route = APIRouter(prefix="/vendedores", tags=["vendedores"])

@route.post('/', response_model=VendedorCreate, status_code=status.HTTP_201_CREATED)
def create_vendedor(body: VendedorCreate, db: Session = Depends(get_db)):
    _vendedor_id = generate_id()

    db_vendedor = db.query(Vendedor).filter(Vendedor.id_vendedor == body.id_vendedor).first()



    db_vendedor = Vendedor(
        id_vendedor=_vendedor_id,
        nome_vendedor=body.nome_vendedor,
        prefixo_cep=body.prefixo_cep,
        cidade=body.cidade,
        estado=body.estado
    )


    db.add(db_vendedor)
    db.commit()
    db.refresh(db_vendedor)
    return db_vendedor

@route.get('/', response_model=list[VendedorRead])
def read_vendedores(db: Session = Depends(get_db)):
    vendedores = db.query(Vendedor).all()
    return vendedores

@route.get('/{nome}', response_model=list[VendedorRead])
def read_vendedor(nome: str, db: Session = Depends(get_db)):
    vendedor = db.query(Vendedor).filter(Vendedor.nome_vendedor.ilike(f"%{nome}%")).all()
    if not vendedor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vendedor não encontrado")
    return vendedor

@route.patch('/{id_vendedor}', response_model=VendedorRead)
def update_vendedor(id_vendedor: str, body: VendedorUpdate, db: Session = Depends(get_db)):
    vendedor = db.query(Vendedor).filter(Vendedor.id_vendedor == id_vendedor).first()
    if not vendedor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vendedor não encontrado")

    for key, value in body.model_dump(exclude_unset=True).items():
        setattr(vendedor, key, value)

    db.commit()
    db.refresh(vendedor)
    return vendedor

@route.delete('/{id_vendedor}', status_code=status.HTTP_204_NO_CONTENT)
def delete_vendedor(id_vendedor: str, db: Session = Depends(get_db)):
    vendedor = db.query(Vendedor).filter(Vendedor.id_vendedor == id_vendedor).first()
    if not vendedor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vendedor não encontrado")

    db.delete(vendedor)
    db.commit()
    return None