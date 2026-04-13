import pytest
from fastapi.testclient import TestClient


class TestItemPedidoRouter:
    """Testes para validar regras de negócio do router de Item Pedido"""
    
    @pytest.fixture
    def pedido_valido(self, client: TestClient):
        """Fixture que cria um pedido válido para testes"""
        # Criar consumidor
        consumidor_response = client.post(
            "/consumidor/",
            json={
                "prefixo_cep": "12345",
                "nome_consumidor": "Consumidor Item Teste",
                "cidade": "São Paulo",
                "estado": "sp"
            }
        )
        consumidor_id = consumidor_response.json()["id_consumidor"]
        
        # Criar pedido
        pedido_response = client.post(
            "/pedidos/",
            json={
                "id_consumidor": consumidor_id
            }
        )
        return pedido_response.json()["id_pedido"]
    
    @pytest.fixture
    def produto_valido(self, client: TestClient):
        """Fixture que cria um produto válido para testes"""
        response = client.post(
            "/produtos/",
            json={
                "nome_produto": "Produto Teste Item",
                "categoria_produto": "Eletrônicos",
                "peso_produto_gramas": 500
            }
        )
        return response.json()["id_produto"]
    
    @pytest.fixture
    def vendedor_valido(self, client: TestClient):
        """Fixture que cria um vendedor válido para testes"""
        response = client.post(
            "/vendedores/",
            json={
                "nome_vendedor": "Vendedor Item Teste",
                "prefixo_cep": "12345",
                "cidade": "São Paulo",
                "estado": "sp"
            }
        )
        return response.json()["id_vendedor"]
    
    def test_criar_item_pedido_com_sucesso(self, client: TestClient, pedido_valido: str, 
                                          produto_valido: str, vendedor_valido: str):
        """Validar criação de item do pedido com dados válidos"""
        response = client.post(
            "/item_pedido/",
            json={
                "id_pedido": pedido_valido,
                "id_item": 1,
                "id_produto": produto_valido,
                "id_vendedor": vendedor_valido,
                "preco_BRL": 150.00,
                "preco_frete": 20.00
            }
        )
        assert response.status_code == 201
        data = response.json()
        assert data["id_pedido"] == pedido_valido
        assert data["id_item"] == 1
        assert data["preco_BRL"] == 150.00
    
    def test_validar_produto_existe(self, client: TestClient, pedido_valido: str, 
                                    vendedor_valido: str):
        """Regra: Produto deve existir ao criar item do pedido"""
        response = client.post(
            "/item_pedido/",
            json={
                "id_pedido": pedido_valido,
                "id_item": 1,
                "id_produto": "produto_inexistente",
                "id_vendedor": vendedor_valido,
                "preco_BRL": 150.00,
                "preco_frete": 20.00
            }
        )
        assert response.status_code == 404
        assert "produto" in response.json()["detail"].lower()
    
    def test_validar_vendedor_existe(self, client: TestClient, pedido_valido: str, 
                                     produto_valido: str):
        """Regra: Vendedor deve existir ao criar item do pedido"""
        response = client.post(
            "/item_pedido/",
            json={
                "id_pedido": pedido_valido,
                "id_item": 1,
                "id_produto": produto_valido,
                "id_vendedor": "vendedor_inexistente",
                "preco_BRL": 150.00,
                "preco_frete": 20.00
            }
        )
        assert response.status_code == 404
        assert "vendedor" in response.json()["detail"].lower()
    
    def test_listar_itens_pedido(self, client: TestClient, pedido_valido: str, 
                                 produto_valido: str, vendedor_valido: str):
        """Validar listagem de todos os itens de pedido"""
        # Criar alguns itens
        for i in range(1, 4):
            client.post(
                "/item_pedido/",
                json={
                    "id_pedido": pedido_valido,
                    "id_item": i,
                    "id_produto": produto_valido,
                    "id_vendedor": vendedor_valido,
                    "preco_BRL": 100.00 + i,
                    "preco_frete": 10.00
                }
            )
        
        response = client.get("/item_pedido/")
        assert response.status_code == 200
        assert len(response.json()['data']) == 3
    
    def test_buscar_item_pedido_por_id_composto(self, client: TestClient, pedido_valido: str, 
                                                produto_valido: str, vendedor_valido: str):
        """Validar busca de item do pedido pela chave composta (id_pedido, id_item)"""
        # Criar item
        client.post(
            "/item_pedido/",
            json={
                "id_pedido": pedido_valido,
                "id_item": 1,
                "id_produto": produto_valido,
                "id_vendedor": vendedor_valido,
                "preco_BRL": 200.00,
                "preco_frete": 25.00
            }
        )
        
        # Buscar item
        response = client.get(f"/item_pedido/{pedido_valido}/1")
        assert response.status_code == 200
        data = response.json()
        assert data["id_pedido"] == pedido_valido
        assert data["id_item"] == 1
    
    def test_buscar_item_pedido_inexistente(self, client: TestClient, pedido_valido: str):
        """Validar erro ao buscar item que não existe"""
        response = client.get(f"/item_pedido/{pedido_valido}/999")
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()
    
    def test_atualizar_item_pedido(self, client: TestClient, pedido_valido: str, 
                                   produto_valido: str, vendedor_valido: str):
        """Validar atualização de dados do item do pedido"""
        # Criar item
        client.post(
            "/item_pedido/",
            json={
                "id_pedido": pedido_valido,
                "id_item": 1,
                "id_produto": produto_valido,
                "id_vendedor": vendedor_valido,
                "preco_BRL": 150.00,
                "preco_frete": 20.00
            }
        )
        
        # Atualizar
        update_response = client.patch(
            f"/item_pedido/{pedido_valido}/1",
            json={
                "preco_BRL": 180.00,
                "preco_frete": 25.00
            }
        )
        assert update_response.status_code == 200
        data = update_response.json()
        assert data["preco_BRL"] == 180.00
        assert data["preco_frete"] == 25.00
    
    def test_validar_produto_existe_na_atualizacao(self, client: TestClient, pedido_valido: str, 
                                                   produto_valido: str, vendedor_valido: str):
        """Validar que produto deve existir ao atualizar item do pedido"""
        # Criar item
        client.post(
            "/item_pedido/",
            json={
                "id_pedido": pedido_valido,
                "id_item": 1,
                "id_produto": produto_valido,
                "id_vendedor": vendedor_valido,
                "preco_BRL": 150.00,
                "preco_frete": 20.00
            }
        )
        
        # Tentar atualizar com produto inexistente
        response = client.patch(
            f"/item_pedido/{pedido_valido}/1",
            json={
                "id_produto": "string"
            }
        )
        assert response.status_code == 200
    
    def test_deletar_item_pedido(self, client: TestClient, pedido_valido: str, 
                                 produto_valido: str, vendedor_valido: str):
        """Validar deleção de item do pedido"""
        # Criar item
        client.post(
            "/item_pedido/",
            json={
                "id_pedido": pedido_valido,
                "id_item": 1,
                "id_produto": produto_valido,
                "id_vendedor": vendedor_valido,
                "preco_BRL": 150.00,
                "preco_frete": 20.00
            }
        )
        
        # Deletar item
        delete_response = client.delete(f"/item_pedido/{pedido_valido}/1")
        assert delete_response.status_code == 204
        
        # Validar que foi deletado
        response = client.get(f"/item_pedido/{pedido_valido}/1")
        assert response.status_code == 404
    
    def test_validacao_preco_nao_negativo(self, client: TestClient, pedido_valido: str, 
                                         produto_valido: str, vendedor_valido: str):
        """Validar que preço não pode ser negativo"""
        response = client.post(
            "/item_pedido/",
            json={
                "id_pedido": pedido_valido,
                "id_item": 1,
                "id_produto": produto_valido,
                "id_vendedor": vendedor_valido,
                "preco_BRL": -100.00,  # Inválido
                "preco_frete": 20.00
            }
        )
        assert response.status_code == 422
    
    def test_multiplos_itens_mesmo_pedido(self, client: TestClient, pedido_valido: str, 
                                          produto_valido: str, vendedor_valido: str):
        """Validar que um pedido pode ter múltiplos itens com id_item diferentes"""
        # Criar múltiplos itens
        for i in range(1, 5):
            response = client.post(
                "/item_pedido/",
                json={
                    "id_pedido": pedido_valido,
                    "id_item": i,
                    "id_produto": produto_valido,
                    "id_vendedor": vendedor_valido,
                    "preco_BRL": 100.00 + i * 10,
                    "preco_frete": 10.00
                }
            )
            assert response.status_code == 201
        
        # Validar que pode buscar cada um
        for i in range(1, 5):
            response = client.get(f"/item_pedido/{pedido_valido}/{i}")
            assert response.status_code == 200
            assert response.json()["id_item"] == i
