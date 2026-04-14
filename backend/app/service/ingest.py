from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import func
import csv
from app.database import SessionLocal, get_db
from app.models import Vendedor, Pedido, AvaliacaoPedido, ItemPedido, Produto, Consumidor
from app.service.utils import calcular_media_avaliacoes, calcular_media_avaliacoes_produto
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


def load_category_images(file_path: str) -> dict:
    """Carrega mapeamento de categorias para links de imagens"""
    category_images = {}
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            category_images[row['Categoria']] = row['Link']
    return category_images


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


def ingest_produtos(db: Session, file_path: str, category_images: dict = None):
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            link_imagem = None
            if category_images and row['categoria_produto'] in category_images:
                link_imagem = category_images[row['categoria_produto']]
            produto = Produto(
                id_produto=row['id_produto'],
                nome_produto=row['nome_produto'],
                categoria_produto=row['categoria_produto'],
                peso_produto_gramas=float(row['peso_produto_gramas']) if row.get('peso_produto_gramas') else None,
                comprimento_centimetros=float(row['comprimento_centimetros']) if row.get('comprimento_centimetros') else None,
                altura_centimetros=float(row['altura_centimetros']) if row.get('altura_centimetros') else None,
                largura_centimetros=float(row['largura_centimetros']) if row.get('largura_centimetros') else None,
                link_imagem=link_imagem
            )
            db.merge(produto)
        db.commit()
    print("✓ Produtos ingeridos com sucesso")


def ingest_clientes(db: Session, file_path: str):
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            existente = db.query(Consumidor).filter(
                Consumidor.id_consumidor == row['id_consumidor']
            ).first()
            if not existente:
                consumidor = Consumidor(
                    id_consumidor=row['id_consumidor'],
                    prefixo_cep=row['prefixo_cep'],
                    nome_consumidor=row['nome_consumidor'],
                    cidade=row['cidade'],
                    estado=row['estado']
                )
                db.add(consumidor)
        db.commit()


def calculate_all_pedido_ratings(db: Session):
    """
    Calcula a média de avaliações para todos os pedidos e atualiza
    o campo media_avaliacoes em Pedido.

    Um pedido pode ter múltiplas avaliações (duplicatas de id_pedido na tabela
    AvaliacaoPedido), por isso agrupamos por id_pedido e tiramos a média.
    """
    print("Calculando médias de pedidos...")

    pedido_medias = (
        db.query(
            AvaliacaoPedido.id_pedido,
            func.avg(AvaliacaoPedido.avaliacao).label('media')
        )
        .group_by(AvaliacaoPedido.id_pedido)
        .all()
    )

    for pedido_id, media in pedido_medias:
        db.query(Pedido).filter(Pedido.id_pedido == pedido_id).update(
            {Pedido.media_avaliacoes: media}
        )

    db.commit()
    print(f"✓ {len(pedido_medias)} pedidos com médias calculadas")


def calculate_all_produto_ratings(db: Session):
    """
    Calcula a média de avaliações para todos os produtos e atualiza
    o campo media_avaliacoes em Produto.

    Cadeia de relações:
        Produto (id_produto)
            → ItemPedido (id_produto = Produto.id_produto)
            → Pedido    (id_pedido  = ItemPedido.id_pedido)
            → AvaliacaoPedido (id_pedido = Pedido.id_pedido)

    O JOIN com ItemPedido era o elo ausente na versão original.
    """
    print("Calculando médias de produtos...")

    produto_medias = (
        db.query(
            Produto.id_produto,
            func.avg(AvaliacaoPedido.avaliacao).label('media_avaliacoes')
        )
        # 1) Produto → ItemPedido
        .join(ItemPedido, ItemPedido.id_produto == Produto.id_produto)
        # 2) ItemPedido → Pedido
        .join(Pedido, Pedido.id_pedido == ItemPedido.id_pedido)
        # 3) Pedido → AvaliacaoPedido
        .join(AvaliacaoPedido, AvaliacaoPedido.id_pedido == Pedido.id_pedido)
        .group_by(Produto.id_produto)
        .all()
    )

    for produto_id, media in produto_medias:
        db.query(Produto).filter(Produto.id_produto == produto_id).update(
            {Produto.media_avaliacoes: media}
        )

    db.commit()
    print(f"✓ {len(produto_medias)} produtos com médias calculadas")


def populate_database(path: str = BASE_DIR / 'data'):
    db = SessionLocal()
    try:
        ingest_vendedores(db, f'{path}/dim_vendedores.csv')
        ingest_pedidos(db, f'{path}/fat_pedidos.csv')

        category_images = load_category_images(f'{path}/dim_categoria_imagens.csv')
        ingest_produtos(db, f'{path}/dim_produtos.csv', category_images)

        ingest_clientes(db, f'{path}/dim_consumidores.csv')
        ingest_avaliacao_pedidos(db, f'{path}/fat_avaliacoes_pedidos.csv')
        ingest_item_pedidos(db, f'{path}/fat_itens_pedidos.csv')

        # Médias de pedidos primeiro (dependência dos produtos)
        calculate_all_pedido_ratings(db)
        calculate_all_produto_ratings(db)

        print("\n✓ Ingestão de dados concluída com sucesso!")
    except Exception as e:
        db.rollback()
        print(f"\n✗ Erro durante a ingestão: {e}")
        raise
    finally:
        db.close()


populate_database()