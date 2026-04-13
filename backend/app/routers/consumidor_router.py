from fastapi import APIRouter, Depends, HTTPException, status, Query
from pytest import skip
from sqlalchemy.orm import Session

from app.database import get_db

from app.models import Consumidor
from app.schema.consumidor_schema import ConsumidorCreate, ConsumidorUpdate, ConsumidorRead
from app.schema.pagination_schema import PaginatedResponse, calculate_pagination


from app.service.utils import generate_id
from app.models.pedido import Pedido

route = APIRouter(prefix="/consumidor", tags=["consumidores"])

@route.post('/', response_model=ConsumidorRead, status_code=status.HTTP_201_CREATED)
def create_consumidor(body: ConsumidorCreate, db: Session = Depends(get_db)):
    _consumidor_id = generate_id()

    db_consumidor = Consumidor(
        id_consumidor=_consumidor_id,
        nome_consumidor=body.nome_consumidor,
        prefixo_cep=body.prefixo_cep,
        cidade=body.cidade,
        estado=body.estado.upper()
    )

    db.add(db_consumidor)
    db.commit()
    db.refresh(db_consumidor)
    return db_consumidor

@route.get('/', response_model=PaginatedResponse[ConsumidorRead])
def read_consumidores(
    skip: int = Query(0, ge=0, description="Items a pular"),
    limit: int = Query(10, ge=1, le=100, description="Items por página"),
    db: Session = Depends(get_db)
):
    total = db.query(Consumidor).count()
    consumidores = db.query(Consumidor).offset(skip).limit(limit).all()
    pagination_info = calculate_pagination(total, skip, limit)
    return PaginatedResponse(
        data=consumidores,
        **pagination_info
    )

@route.get('/{nome}', response_model=list[ConsumidorRead])
def read_consumidor(nome: str, db: Session = Depends(get_db)):
    consumidor = db.query(Consumidor).filter(Consumidor.nome_consumidor.ilike(f"%{nome}%")).all()
    if not consumidor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Consumidor não encontrado")
    return consumidor

@route.patch('/{id_consumidor}', response_model=ConsumidorRead)
def update_consumidor(id_consumidor: str, body: ConsumidorUpdate, db: Session = Depends(get_db)):
    consumidor = db.query(Consumidor).filter(Consumidor.id_consumidor == id_consumidor).first()
    if not consumidor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Consumidor não encontrado")

    if body.estado:
        body.estado = body.estado.upper()

    for key, value in body.model_dump(exclude_unset=True).items():
        setattr(consumidor, key, value)

    db.commit()
    db.refresh(consumidor)
    return consumidor

@route.delete('/{id_consumidor}', status_code=status.HTTP_204_NO_CONTENT)
def delete_consumidor(id_consumidor: str, db: Session = Depends(get_db)):
    consumidor = db.query(Consumidor).filter(Consumidor.id_consumidor == id_consumidor).first()
    if not consumidor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Consumidor não encontrado")
    
    avaliacoes = db.query(Pedido).filter(Pedido.id_consumidor == id_consumidor).all()
    if avaliacoes:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Não é possível deletar um consumidor com pedidos associados")

    db.delete(consumidor)
    db.commit()

