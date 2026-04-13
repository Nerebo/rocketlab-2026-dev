import pytest
from fastapi.testclient import TestClient


class TestVendedorRouter:
    """Testes para validar regras de negócio do router de Vendedor"""
    
    def test_criar_vendedor_com_sucesso(self, client: TestClient):
        """Validar criação de vendedor com dados válidos"""
        response = client.post(
            "/vendedores/",
            json={
                "nome_vendedor": "TechStore São Paulo",
                "prefixo_cep": "01013",
                "cidade": "São Paulo",
                "estado": "sp"
            }
        )
        assert response.status_code == 201
        data = response.json()
        assert data["nome_vendedor"] == "TechStore São Paulo"
        assert "id_vendedor" in data
    
    
    def test_listar_vendedores(self, client: TestClient):
        """Validar listagem de todos os vendedores"""
        # Criar alguns vendedores
        for i in range(3):
            client.post(
                "/vendedores/",
                json={
                    "nome_vendedor": f"Vendedor {i}",
                    "prefixo_cep": f"0000{i}",
                    "cidade": "São Paulo",
                    "estado": "sp"
                }
            )
        
        response = client.get("/vendedores/")
        assert response.status_code == 200
        assert len(response.json()['data']) == 3
    
    def test_buscar_vendedor_por_nome(self, client: TestClient):
        """Validar busca de vendedor por nome (case-insensitive)"""
        # Criar vendedor
        client.post(
            "/vendedores/",
            json={
                "nome_vendedor": "Importadora Chinesa",
                "prefixo_cep": "25000",
                "cidade": "Duque de Caxias",
                "estado": "rj"
            }
        )
        
        # Buscar com nome parcial e diferentes cases
        response = client.get("/vendedores/importadora")
        assert response.status_code == 200
        assert len(response.json()) > 0
        
        response = client.get("/vendedores/CHINESA")
        assert response.status_code == 200
        assert len(response.json()) > 0
    
    def test_buscar_vendedor_nao_existente(self, client: TestClient):
        """Validar que busca de vendedor inexistente retorna erro 404"""
        response = client.get("/vendedores/vendedor_inexistente")
        assert response.status_code == 404
        assert "não encontrado" in response.json()["detail"].lower()
    
    def test_atualizar_vendedor(self, client: TestClient):
        """Validar atualização de dados do vendedor"""
        # Criar vendedor
        create_response = client.post(
            "/vendedores/",
            json={
                "nome_vendedor": "Loja Premium",
                "prefixo_cep": "30000",
                "cidade": "Belo Horizonte",
                "estado": "mg"
            }
        )
        vendedor_id = create_response.json()["id_vendedor"]
        
        # Atualizar
        update_response = client.patch(
            f"/vendedores/{vendedor_id}",
            json={
                "nome_vendedor": "Loja Premium Plus",
                "cidade": "Contagem",
                "estado": "mg"
            }
        )
        assert update_response.status_code == 200
        data = update_response.json()
        assert data["nome_vendedor"] == "Loja Premium Plus"
        assert data["cidade"] == "Contagem"
        assert data["estado"] == "MG"  # Deve estar em maiúsculas
    
    def test_atualizar_vendedor_inexistente(self, client: TestClient):
        """Validar erro ao tentar atualizar vendedor que não existe"""
        response = client.patch(
            "/vendedores/id_inexistente",
            json={"nome_vendedor": "Novo Nome"}
        )
        assert response.status_code == 404
    
    def test_deletar_vendedor(self, client: TestClient):
        """Validar deleção de vendedor"""
        # Criar vendedor
        create_response = client.post(
            "/vendedores/",
            json={
                "nome_vendedor": "Loja Descartável",
                "prefixo_cep": "40000",
                "cidade": "Salvador",
                "estado": "ba"
            }
        )
        vendedor_id = create_response.json()["id_vendedor"]
        
        # Deletar vendedor
        delete_response = client.delete(f"/vendedores/{vendedor_id}")
        assert delete_response.status_code == 204
        
        # Validar que foi deletado
        response = client.get("/vendedores/Loja Descartável")
        assert response.status_code == 404
    
    def test_deletar_vendedor_inexistente(self, client: TestClient):
        """Validar erro ao deletar vendedor que não existe"""
        response = client.delete("/vendedores/id_inexistente")
        assert response.status_code == 404
    
    def test_validacao_estado_dois_caracteres(self, client: TestClient):
        """Validar que estado deve ter exatamente 2 caracteres"""
        response = client.post(
            "/vendedores/",
            json={
                "nome_vendedor": "Loja Test",
                "prefixo_cep": "00000",
                "cidade": "Cidade",
                "estado": "s"  # Inválido - apenas 1 caractere
            }
        )
        assert response.status_code == 422
    
    def test_validacao_nome_nao_vazio(self, client: TestClient):
        """Validar que nome do vendedor não pode ser vazio"""
        response = client.post(
            "/vendedores/",
            json={
                "nome_vendedor": "",
                "prefixo_cep": "00000",
                "cidade": "Cidade",
                "estado": "sp"
            }
        )
        assert response.status_code == 422
