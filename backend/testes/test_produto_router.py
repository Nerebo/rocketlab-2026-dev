import pytest
from fastapi.testclient import TestClient


class TestProdutoRouter:
    """Testes para validar regras de negócio do router de Produto"""
    
    def test_criar_produto_com_sucesso(self, client: TestClient):
        """Validar criação de produto com dados válidos"""
        response = client.post(
            "/produtos/",
            json={
                "nome_produto": "Notebook Dell XPS",
                "categoria_produto": "Eletrônicos",
                "peso_produto_gramas": 2500,
                "comprimento_centimetros": 36,
                "altura_centimetros": 2.5,
                "largura_centimetros": 25
            }
        )
        assert response.status_code == 201
        data = response.json()
        assert data["nome_produto"] == "Notebook Dell XPS"
        assert data["categoria_produto"] == "Eletrônicos"
        assert "id_produto" in data
    
    def test_criar_produto_com_dados_parciais(self, client: TestClient):
        """Validar criação de produto com apenas dados obrigatórios"""
        response = client.post(
            "/produtos/",
            json={
                "nome_produto": "Mouse Óptico",
                "categoria_produto": "Periféricos"
            }
        )
        assert response.status_code == 201
        data = response.json()
        assert data["nome_produto"] == "Mouse Óptico"
        assert data["peso_produto_gramas"] is None
    
    def test_listar_produtos(self, client: TestClient):
        """Validar listagem de todos os produtos"""
        # Criar alguns produtos
        for i in range(3):
            client.post(
                "/produtos/",
                json={
                    "nome_produto": f"Produto {i}",
                    "categoria_produto": "Categoria Test"
                }
            )
        
        response = client.get("/produtos/")
        assert response.status_code == 200
        assert len(response.json()['data']) == 3
    
    def test_buscar_produto_por_nome(self, client: TestClient):
        """Validar busca de produto por nome (case-insensitive)"""
        # Criar produto
        client.post(
            "/produtos/",
            json={
                "nome_produto": "teclado",
                "categoria_produto": "string",
                "peso_produto_gramas": 1,
                "comprimento_centimetros": 1,
                "altura_centimetros": 1,
                "largura_centimetros": 1
                }
        )
        
        # Buscar com nome parcial
        response = client.get("/produtos/buscar/teclado")
        assert response.status_code == 200
        assert len(response.json()) > 0
        
        # Buscar com diferentes cases
        response = client.get("/produtos/buscar/TECLADO")
        assert response.status_code == 200
        assert len(response.json()) > 0
    
    def test_buscar_produto_nao_existente(self, client: TestClient):
        """Validar que busca de produto inexistente retorna erro 404"""
        response = client.get("/produtos/buscar/produto_inexistente_xyz")
        assert response.status_code == 404
        assert "não encontrado" in response.json()["detail"].lower()
    
    def test_atualizar_produto(self, client: TestClient):
        """Validar atualização de dados do produto"""
        # Criar produto
        create_response = client.post(
            "/produtos/",
            json={
                "nome_produto": "Monitor LG 27 polegadas",
                "categoria_produto": "Monitores",
                "peso_produto_gramas": 5000
            }
        )
        produto_id = create_response.json()["id_produto"]
        
        # Atualizar
        update_response = client.patch(
            f"/produtos/{produto_id}",
            json={
                "peso_produto_gramas": 4800,
                "altura_centimetros": 42
            }
        )
        assert update_response.status_code == 200
        data = update_response.json()
        assert data["peso_produto_gramas"] == 4800
        assert data["altura_centimetros"] == 42
    
    def test_atualizar_produto_inexistente(self, client: TestClient):
        """Validar erro ao tentar atualizar produto que não existe"""
        response = client.patch(
            "/produtos/id_inexistente",
            json={"peso_produto_gramas": 1000}
        )
        assert response.status_code == 404
    
    def test_deletar_produto(self, client: TestClient):
        """Validar deleção de produto"""
        # Criar produto
        create_response = client.post(
            "/produtos/",
            json={
                "nome_produto": "Webcam HD",
                "categoria_produto": "Periféricos"
            }
        )
        produto_id = create_response.json()["id_produto"]
        
        # Deletar produto
        delete_response = client.delete(f"/produtos/{produto_id}")
        assert delete_response.status_code == 204
        
        # Validar que foi deletado
        response = client.get(f"/produtos/buscar/Webcam HD")
        assert response.status_code == 404
    
    def test_deletar_produto_inexistente(self, client: TestClient):
        """Validar erro ao deletar produto que não existe"""
        response = client.delete("/produtos/id_inexistente")
        assert response.status_code == 404
    
    def test_validacao_peso_positivo(self, client: TestClient):
        """Validar que peso deve ser positivo"""
        response = client.post(
            "/produtos/",
            json={
                "nome_produto": "Produto Invalid",
                "categoria_produto": "Test",
                "peso_produto_gramas": -100  # Inválido
            }
        )
        assert response.status_code == 422  # Validation error
    
    def test_validacao_dimensoes_positivas(self, client: TestClient):
        """Validar que dimensões devem ser positivas"""
        response = client.post(
            "/produtos/",
            json={
                "nome_produto": "Produto Invalid",
                "categoria_produto": "Test",
                "altura_centimetros": 0  # Inválido
            }
        )
        assert response.status_code == 422  # Validation error
