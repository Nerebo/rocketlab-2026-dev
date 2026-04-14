import hashlib
import random
from sqlalchemy.orm import Session
from app.models import AvaliacaoPedido, Pedido, ItemPedido, Produto
from sqlalchemy import func

def generate_id():
    palavras = [
        "casa", "carro", "janela", "porta", "livro", "mesa", "cadeira", "computador", "teclado", "mouse",
        "monitor", "celular", "internet", "rede", "servidor", "cliente", "banco", "dados", "arquivo", "pasta",
        "código", "programa", "função", "classe", "objeto", "variável", "lista", "dicionario", "tupla", "string",
        "inteiro", "float", "booleano", "verdadeiro", "falso", "condicao", "loop", "while", "for", "if",
        "else", "elif", "import", "modulo", "pacote", "sistema", "usuario", "senha", "login", "seguranca"
    ]

    tres_palavras = random.sample(palavras, 3)
    id_string = ''.join(tres_palavras)

    # Randomiza maiúsculo/minúsculo por caractere
    id_random = ''.join(
        ch.upper() if random.choice([True, False]) else ch.lower()
        for ch in id_string
    )

    return(hashlib.md5(id_random.encode()).hexdigest())


def calcular_media_avaliacoes(db: Session, id_pedido: str) -> float:
    """
    Calcula a média de avaliações de um pedido e atualiza o campo media_avaliacoes.
    
    Args:
        db: Sessão do SQLAlchemy
        id_pedido: ID do pedido
        
    Returns:
        A média de avaliações calculada
    """
    # Calcula a média de avaliações do pedido
    media = db.query(func.avg(AvaliacaoPedido.avaliacao)).filter(
        AvaliacaoPedido.id_pedido == id_pedido
    ).scalar()
    
    # Se não houver avaliações, media será None
    if media is None:
        media = 0.0
    else:
        media = float(media)
    
    # Atualiza o pedido com a nova média
    pedido = db.query(Pedido).filter(Pedido.id_pedido == id_pedido).first()
    if pedido:
        pedido.media_avaliacoes = media
        db.commit()
    
    return media


def calcular_media_avaliacoes_produto(db: Session, id_produto: str) -> float:
    """
    Calcula a média de avaliações de um produto baseado nas médias dos pedidos que o contêm.
    
    Args:
        db: Sessão do SQLAlchemy
        id_produto: ID do produto
        
    Returns:
        A média de avaliações calculada
    """
    # Busca todos os pedidos que contêm este produto
    pedidos_ids = db.query(ItemPedido.id_pedido).filter(
        ItemPedido.id_produto == id_produto
    ).all()
    
    pedidos_ids = [p[0] for p in pedidos_ids]
    
    if not pedidos_ids:
        # Sem pedidos, média é 0
        produto = db.query(Produto).filter(Produto.id_produto == id_produto).first()
        if produto:
            produto.media_avaliacoes = 0.0
            db.commit()
        return 0.0
    
    # Calcula a média das médias de avaliação dos pedidos
    media = db.query(func.avg(Pedido.media_avaliacoes)).filter(
        Pedido.id_pedido.in_(pedidos_ids)
    ).scalar()
    
    if media is None:
        media = 0.0
    else:
        media = float(media)
    
    # Atualiza o produto com a nova média
    produto = db.query(Produto).filter(Produto.id_produto == id_produto).first()
    if produto:
        produto.media_avaliacoes = media
        db.commit()
    
    return media