import pytest
from fastapi.testclient import TestClient
from datetime import datetime


class TestPedidoRouter:
    """Testes para validar regras de negócio do router de Pedido"""
    
    @pytest.fixture
    def consumidor_valido(self, client: TestClient):
        """Fixture que cria um consumidor válido para testes"""
        response = client.post(
            "/consumidor/",
            json={
                "prefixo_cep": "12345",
                "nome_consumidor": "Consumidor Teste",
                "cidade": "São Paulo",
                "estado": "sp"
            }
        )
        return response.json()["id_consumidor"]
    
    def test_criar_pedido_com_sucesso(self, client: TestClient, consumidor_valido: str):
        """Validar criação de pedido com consumidor válido"""
        response = client.post(
            "/pedidos/",
            json={
                "id_consumidor": consumidor_valido
            }
        )
        assert response.status_code == 201
        data = response.json()
        assert data["id_consumidor"] == consumidor_valido
        assert "id_pedido" in data
    
    def test_pedido_com_consumidor_inexistente(self, client: TestClient):
        """Regra: Não permitir criar pedido com consumidor que não existe"""
        response = client.post(
            "/pedidos/",
            json={
                "id_consumidor": "consumidor_inexistente"
            }
        )
        assert response.status_code == 404
        assert "consumidor" in response.json()["detail"].lower()
    
    def test_status_inicial_criado(self, client: TestClient, consumidor_valido: str):
        """Regra: Pedido criado deve ter status = 'criado'"""
        response = client.post(
            "/pedidos/",
            json={
                "id_consumidor": consumidor_valido
            }
        )
        assert response.status_code == 201
        data = response.json()
        assert data["status"] == "criado"
    
    def test_pedido_compra_timestamp(self, client: TestClient, consumidor_valido: str):
        """Validar que pedido_compra_timestamp é preenchido ao criar"""
        response = client.post(
            "/pedidos/",
            json={
                "id_consumidor": consumidor_valido
            }
        )
        assert response.status_code == 201
        data = response.json()
        assert data["pedido_compra_timestamp"] is not None
    
    def test_listar_pedidos(self, client: TestClient, consumidor_valido: str):
        """Validar listagem de pedidos (máximo 100)"""
        # Criar alguns pedidos
        for i in range(3):
            client.post(
                "/pedidos/",
                json={
                    "id_consumidor": consumidor_valido
                }
            )
        
        response = client.get("/pedidos/")
        assert response.status_code == 200
        assert len(response.json()) == 3
    
    def test_buscar_pedido_por_id(self, client: TestClient, consumidor_valido: str):
        """Validar busca de pedido pelo ID"""
        # Criar pedido
        create_response = client.post(
            "/pedidos/",
            json={
                "id_consumidor": consumidor_valido
            }
        )
        pedido_id = create_response.json()["id_pedido"]
        
        # Buscar pedido
        response = client.get(f"/pedidos/{pedido_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id_pedido"] == pedido_id
    
    def test_buscar_pedido_inexistente(self, client: TestClient):
        """Validar erro ao buscar pedido que não existe"""
        response = client.get("/pedidos/pedido_inexistente")
        assert response.status_code == 404
        assert "não encontrado" in response.json()["detail"].lower()
    
    def test_atualizar_status_valido(self, client: TestClient, consumidor_valido: str):
        """Validar atualização de status para valores permitidos"""
        # Criar pedido
        create_response = client.post(
            "/pedidos/",
            json={
                "id_consumidor": consumidor_valido
            }
        )
        pedido_id = create_response.json()["id_pedido"]
        
        # Atualizar para status válido
        status_valido = "enviado"
        update_response = client.patch(
            f"/pedidos/{pedido_id}",
            json={"status": status_valido}
        )
        assert update_response.status_code == 200
        data = update_response.json()
        assert data["status"] == status_valido
    
    def test_nao_deletar_pedido_com_avaliacoes(self, client: TestClient, consumidor_valido: str):
        """Regra: Não permitir deletar pedido que possui avaliações associadas"""
        # Criar pedido
        create_response = client.post(
            "/pedidos/",
            json={
                "id_consumidor": consumidor_valido
            }
        )
        pedido_id = create_response.json()["id_pedido"]
        
        # Criar avaliação para este pedido
        avaliacao_response = client.post(
            "/avaliacao_pedidos/",
            json={
                "id_pedido": pedido_id,
                "avaliacao": 5,
                "titulo_comentario": "Excelente",
                "comentario": "Produto de qualidade"
            }
        )
        assert avaliacao_response.status_code == 201
        
        # Tentar deletar pedido com avaliação
        delete_response = client.delete(f"/pedidos/{pedido_id}")
        assert delete_response.status_code == 400
        assert "avaliações associadas" in delete_response.json()["detail"].lower()
    
    def test_deletar_pedido_sem_avaliacoes(self, client: TestClient, consumidor_valido: str):
        """Validar que pode deletar pedido sem avaliações"""
        # Criar pedido
        create_response = client.post(
            "/pedidos/",
            json={
                "id_consumidor": consumidor_valido
            }
        )
        pedido_id = create_response.json()["id_pedido"]
        
        # Deletar pedido
        delete_response = client.delete(f"/pedidos/{pedido_id}")
        assert delete_response.status_code == 204
        
        # Validar que foi deletado
        response = client.get(f"/pedidos/{pedido_id}")
        assert response.status_code == 404
    
    def test_deletar_pedido_inexistente(self, client: TestClient):
        """Validar erro ao deletar pedido que não existe"""
        response = client.delete("/pedidos/pedido_inexistente")
        assert response.status_code == 404
    
    def test_atualizar_timestamps(self, client: TestClient, consumidor_valido: str):
        """Validar atualização de timestamps do pedido"""
        # Criar pedido
        create_response = client.post(
            "/pedidos/",
            json={
                "id_consumidor": consumidor_valido
            }
        )
        pedido_id = create_response.json()["id_pedido"]
        
        # Atualizar timestamps
        nova_data = datetime.now().isoformat()
        update_response = client.patch(
            f"/pedidos/{pedido_id}",
            json={
                "pedido_entregue_timestamp": nova_data,
                "status": "entregue"
            }
        )
        assert update_response.status_code == 200
        data = update_response.json()
        assert data["status"] == "entregue"
