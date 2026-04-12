from fastapi import APIRouter, Depends, HTTPException, status
from pytest import skip
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import ItemPedido
from app.schema.item_pedido_schema import ItemPedidoCreate, ItemPedidoUpdate, ItemPedidoRead

router = APIRouter(prefix="/item_pedido", tags=["item_pedido"])

@router.post("/", response_model=ItemPedidoRead, status_code=status.HTTP_201_CREATED)
def create_item_pedido(item_pedido: ItemPedidoCreate, db: Session = Depends(get_db)):
    db_item_pedido = ItemPedido(**item_pedido.dict())
    db.add(db_item_pedido)
    db.commit()
    db.refresh(db_item_pedido)
    return db_item_pedido

@router.get("/", response_model=list[ItemPedidoRead])
def read_item_pedidos(db: Session = Depends(get_db)):
    return db.query(ItemPedido).all()

@router.get("/{item_pedido_id}", response_model=ItemPedidoRead)
def read_item_pedido(item_pedido_id: int, db: Session = Depends(get_db)):
    db_item_pedido = db.query(ItemPedido).filter(ItemPedido.id == item_pedido_id).first()
    if db_item_pedido is None:
        raise HTTPException(status_code=404, detail="ItemPedido not found")
    return db_item_pedido

@router.patch("/{item_pedido_id}", response_model=ItemPedidoRead)
def update_item_pedido(item_pedido_id: int, item_pedido: ItemPedidoUpdate, db: Session = Depends(get_db)):
    db_item_pedido = db.query(ItemPedido).filter(ItemPedido.id == item_pedido_id).first()
    if db_item_pedido is None:
        raise HTTPException(status_code=404, detail="ItemPedido not found")
    for key, value in item_pedido.model_dump(exclude_unset=True).items():
        setattr(db_item_pedido, key, value)
    db.commit()
    db.refresh(db_item_pedido)
    return db_item_pedido

@router.delete("/{item_pedido_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item_pedido(item_pedido_id: int, db: Session = Depends(get_db)):
    db_item_pedido = db.query(ItemPedido).filter(ItemPedido.id == item_pedido_id).first()
    if db_item_pedido is None:
        raise HTTPException(status_code=404, detail="ItemPedido not found")
    db.delete(db_item_pedido)
    db.commit()
    return None