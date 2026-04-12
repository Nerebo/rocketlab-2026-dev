import pytest
import sys
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from fastapi.testclient import TestClient

# Use um arquivo de teste em vez de memory para evitar problemas com threads
os.environ["DATABASE_URL"] = "sqlite:///./test.db"

# Importar depois de setar variável de ambiente
from app.config import settings
from app.database import Base, get_db, engine as original_engine, SessionLocal as original_sessionlocal
from app.models import (
    Consumidor, Produto, Vendedor, Pedido, ItemPedido, AvaliacaoPedido
)
from app.main import app as fastapi_app

# Criar as tabelas no banco de testes
Base.metadata.create_all(bind=original_engine)

def override_get_db():
    """Override da dependência get_db para usar o banco de testes"""
    try:
        db = original_sessionlocal()
        yield db
    finally:
        db.close()


@pytest.fixture(autouse=True)
def clean_database():
    """Limpa o banco de dados antes e depois de cada teste"""
    # Limpa antes
    with original_engine.begin() as connection:
        for table in reversed(Base.metadata.sorted_tables):
            try:
                connection.execute(table.delete())
            except Exception:
                pass
    
    yield
    
    # Limpa depois
    with original_engine.begin() as connection:
        for table in reversed(Base.metadata.sorted_tables):
            try:
                connection.execute(table.delete())
            except Exception:
                pass


@pytest.fixture
def db() -> Session:
    """Fixture que fornece uma sessão do banco de dados para testes"""
    db = original_sessionlocal()
    yield db
    db.close()


@pytest.fixture
def client():
    """Fixture que fornece um cliente TestClient com banco de dados de teste"""
    fastapi_app.dependency_overrides[get_db] = override_get_db
    client = TestClient(fastapi_app)
    yield client
    fastapi_app.dependency_overrides.clear()


# Limpar o banco de testes ao final
@pytest.fixture(scope="session", autouse=True)
def cleanup_test_db():
    """Limpa o arquivo do banco de testes ao final."""
    yield
    if os.path.exists("test.db"):
        os.remove("test.db")
