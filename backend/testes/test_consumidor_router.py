import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session


class TestConsumidorRouter:
    """Testes para validar regras de negócio do router de Consumidor"""
    
    def test_criar_consumidor_com_sucesso(self, client: TestClient):
        """Validar criação de consumidor com dados válidos"""
        response = client.post(
            "/consumidor/",
            json={
                "prefixo_cep": "12345",
                "nome_consumidor": "João Silva",
                "cidade": "São Paulo",
                "estado": "sp"
            }
        )
        assert response.status_code == 201
        data = response.json()
        assert data["nome_consumidor"] == "João Silva"
        assert "id_consumidor" in data
    
    def test_estado_salvo_em_maiusculas(self, client: TestClient):
        """Regra: Estado deve ser salvo em MAIÚSCULAS"""
        response = client.post(
            "/consumidor/",
            json={
                "prefixo_cep": "12345",
                "nome_consumidor": "Maria Santos",
                "cidade": "Rio de Janeiro",
                "estado": "rj"
            }
        )
        assert response.status_code == 201
        data = response.json()
        assert data["estado"] == "RJ", "Estado não foi convertido para maiúsculas"
    
    def test_listar_consumidores(self, client: TestClient):
        """Validar listagem de todos os consumidores"""
        # Criar alguns consumidores
        for i in range(3):
            client.post(
                "/consumidor/",
                json={
                    "prefixo_cep": f"1234{i}",
                    "nome_consumidor": f"Consumidor {i}",
                    "cidade": "São Paulo",
                    "estado": "sp"
                }
            )
        
        response = client.get("/consumidor/")
        assert response.status_code == 200
        assert len(response.json()) == 3
    
    def test_buscar_consumidor_por_nome(self, client: TestClient):
        """Validar busca de consumidor por nome (case-insensitive)"""
        # Criar consumidor
        client.post(
            "/consumidor/",
            json={
                "prefixo_cep": "12345",
                "nome_consumidor": "Pedro Oliveira",
                "cidade": "Belo Horizonte",
                "estado": "mg"
            }
        )
        
        # Buscar com nome parcial e diferentes cases
        response = client.get("/consumidor/pedro")
        assert response.status_code == 200
        assert len(response.json()) > 0
        
        response = client.get("/consumidor/OLIVEIRA")
        assert response.status_code == 200
        assert len(response.json()) > 0
    
    def test_buscar_consumidor_nao_existente(self, client: TestClient):
        """Validar que busca de consumidor inexistente retorna erro 404"""
        response = client.get("/consumidor/consumidor_inexistente")
        assert response.status_code == 404
        assert "não encontrado" in response.json()["detail"].lower()
    
    def test_atualizar_consumidor(self, client: TestClient):
        """Validar atualização de dados do consumidor"""
        # Criar consumidor
        create_response = client.post(
            "/consumidor/",
            json={
                "prefixo_cep": "12345",
                "nome_consumidor": "Ana Costa",
                "cidade": "Salvador",
                "estado": "ba"
            }
        )
        consumidor_id = create_response.json()["id_consumidor"]
        
        # Atualizar
        update_response = client.patch(
            f"/consumidor/{consumidor_id}",
            json={
                "cidade": "Brasília",
                "estado": "df"
            }
        )
        assert update_response.status_code == 200
        data = update_response.json()
        assert data["cidade"] == "Brasília"
        assert data["estado"] == "DF"  # Deve estar em maiúsculas
    
    def test_atualizar_consumidor_inexistente(self, client: TestClient):
        """Validar erro ao tentar atualizar consumidor que não existe"""
        response = client.patch(
            "/consumidor/id_inexistente",
            json={"cidade": "Nova Cidade"}
        )
        assert response.status_code == 404
    
    def test_nao_deletar_consumidor_com_pedidos(self, client: TestClient):
        """Regra: Não permitir deletar consumidor que tem pedidos associados"""
        from app.models.consumidor import Consumidor
        from app.models.pedido import Pedido
        from datetime import datetime
        
        # Criar consumidor
        create_response = client.post(
            "/consumidor/",
            json={
                "prefixo_cep": "12345",
                "nome_consumidor": "Lucas Ferreira",
                "cidade": "Curitiba",
                "estado": "pr"
            }
        )
        consumidor_id = create_response.json()["id_consumidor"]
        
        # Criar pedido para este consumidor via API
        response = client.post(
            "/pedidos/",
            json={
                "id_consumidor": consumidor_id
            }
        )
        assert response.status_code == 201
        
        # Tentar deletar consumidor com pedido
        delete_response = client.delete(f"/consumidor/{consumidor_id}")
        assert delete_response.status_code == 400
        assert "pedidos associados" in delete_response.json()["detail"].lower()
    
    def test_deletar_consumidor_sem_pedidos(self, client: TestClient):
        """Validar que pode deletar consumidor sem pedidos"""
        # Criar consumidor
        create_response = client.post(
            "/consumidor/",
            json={
                "prefixo_cep": "12345",
                "nome_consumidor": "Felipe Gomes",
                "cidade": "Fortaleza",
                "estado": "ce"
            }
        )
        consumidor_id = create_response.json()["id_consumidor"]
        
        # Deletar consumidor
        delete_response = client.delete(f"/consumidor/{consumidor_id}")
        assert delete_response.status_code == 204
        
        # Validar que foi deletado
        response = client.get(f"/consumidor/Felipe Gomes")
        assert response.status_code == 404
