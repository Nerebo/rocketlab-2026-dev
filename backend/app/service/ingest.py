from datetime import datetime

from sqlalchemy.orm import Session
import csv
from app.database import SessionLocal, get_db
from app.models import Vendedor, Pedido, AvaliacaoPedido, ItemPedido, Produto, Consumidor
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]

def parse_dt(value: str | None):
    if not value:
        return None
    try:
        return datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
    except ValueError:
        return None

def parse_date(value: str | None):
    if not value:
        return None
    try:
        return datetime.strptime(value, '%Y-%m-%d').date()
    except ValueError:
        return None


def ingest_vendedores(db: Session, file_path: str):
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            vendedor = Vendedor(
                id_vendedor=row['id_vendedor'],
                nome_vendedor=row['nome_vendedor'],
                prefixo_cep=row['prefixo_cep'],
                cidade=row['cidade'],
                estado=row['estado']
            )
            db.merge(vendedor)
        db.commit()

def ingest_pedidos(db: Session, file_path: str):
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            pedido = Pedido(
                id_pedido=row['id_pedido'],
                id_consumidor=row['id_consumidor'],
                status=row['status'],
                pedido_compra_timestamp=parse_dt(row.get('pedido_compra_timestamp')),
                pedido_entregue_timestamp=parse_dt(row.get('pedido_entregue_timestamp')),
                data_estimada_entrega=parse_date(row.get('data_estimada_entrega')),
                tempo_entrega_dias=float(row['tempo_entrega_dias']) if row.get('tempo_entrega_dias') else None,
                tempo_entrega_estimado_dias=float(row['tempo_entrega_estimado_dias']) if row.get('tempo_entrega_estimado_dias') else None,
                diferenca_entrega_dias=float(row['diferenca_entrega_dias']) if row.get('diferenca_entrega_dias') else None,
                entrega_no_prazo=row.get('entrega_no_prazo')
            )
            db.merge(pedido)
        db.commit()
    
def ingest_avaliacao_pedidos(db: Session, file_path: str):
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        seen = set()
        for row in reader:
            id_av = row['id_avaliacao']
            if id_av in seen:
                continue
            seen.add(id_av)

            existente = db.get(AvaliacaoPedido, id_av)
            if existente:
                existente.avaliacao = int(row['avaliacao'])
                existente.titulo_comentario = row.get('titulo_comentario')
                existente.comentario = row.get('comentario')
                existente.data_comentario = parse_dt(row.get('data_comentario'))
                existente.data_resposta = parse_dt(row.get('data_resposta'))
            else:
                db.add(AvaliacaoPedido(
                    id_avaliacao=id_av,
                    id_pedido=row['id_pedido'],
                    avaliacao=int(row['avaliacao']),
                    titulo_comentario=row.get('titulo_comentario'),
                    comentario=row.get('comentario'),
                    data_comentario=parse_dt(row.get('data_comentario')),
                    data_resposta=parse_dt(row.get('data_resposta'))
                ))
        db.commit()
        
def ingest_item_pedidos(db: Session, file_path: str):
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            item_pedido = ItemPedido(
                id_pedido=row['id_pedido'],
                id_item=int(row['id_item']),
                id_produto=row['id_produto'],
                id_vendedor=row['id_vendedor'],
                preco_BRL=float(row['preco_BRL']),
                preco_frete=float(row['preco_frete'])
            )
            db.merge(item_pedido)
        db.commit()

def ingest_produtos(db: Session, file_path: str):
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            produto = Produto(
                id_produto=row['id_produto'],
                nome_produto=row['nome_produto'],
                categoria_produto=row['categoria_produto'],
                peso_produto_gramas=float(row['peso_produto_gramas']) if row.get('peso_produto_gramas') else None,
                comprimento_centimetros=float(row['comprimento_centimetros']) if row.get('comprimento_centimetros') else None,
                altura_centimetros=float(row['altura_centimetros']) if row.get('altura_centimetros') else None,
                largura_centimetros=float(row['largura_centimetros']) if row.get('largura_centimetros') else None
            )
            db.merge(produto)
        db.commit()
    
def ingest_clientes(db: Session, file_path: str):
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            consumidor = Consumidor(
                id_consumidor=row['id_consumidor'],
                prefixo_cep=row['prefixo_cep'],
                nome_consumidor=row['nome_consumidor'],
                cidade=row['cidade'],
                estado=row['estado']
            )
            db.merge(consumidor)
        db.commit()

def populate_database(path: str = BASE_DIR / 'data'):
    from app.database import SessionLocal    
    db = SessionLocal()
    ingest_vendedores(db, f'{path}/dim_vendedores.csv')
    ingest_pedidos(db, f'{path}/fat_pedidos.csv')
    ingest_produtos(db, f'{path}/dim_produtos.csv')
    ingest_clientes(db, f'{path}/dim_consumidores.csv')
    
    ingest_avaliacao_pedidos(db, f'{path}/fat_avaliacoes_pedidos.csv')
    ingest_item_pedidos(db, f'{path}/fat_itens_pedidos.csv')

populate_database()