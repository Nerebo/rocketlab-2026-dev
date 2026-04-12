import pytest
from fastapi.testclient import TestClient


class TestAvaliacaoPedidoRouter:
    """Testes para validar regras de negócio do router de Avaliação do Pedido"""
    
    @pytest.fixture
    def pedido_valido(self, client: TestClient):
        """Fixture que cria um pedido válido para testes"""
        # Criar consumidor
        consumidor_response = client.post(
            "/consumidor/",
            json={
                "prefixo_cep": "12345",
                "nome_consumidor": "Consumidor Avaliação",
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
    
    def test_criar_avaliacao_com_sucesso(self, client: TestClient, pedido_valido: str):
        """Validar criação de avaliação com dados válidos"""
        response = client.post(
            "/avaliacao_pedidos/",
            json={
                "id_pedido": pedido_valido,
                "avaliacao": 5,
                "titulo_comentario": "Excelente Produto",
                "comentario": "Produto de ótima qualidade, recomendo!"
            }
        )
        assert response.status_code == 201
        data = response.json()
        assert data["id_pedido"] == pedido_valido
        assert data["avaliacao"] == 5
        assert "id_avaliacao" in data
    
    def test_validar_pedido_existe(self, client: TestClient):
        """Regra: Pedido deve existir ao criar avaliação"""
        response = client.post(
            "/avaliacao_pedidos/",
            json={
                "id_pedido": "pedido_inexistente",
                "avaliacao": 5,
                "titulo_comentario": "Título",
                "comentario": "Comentário"
            }
        )
        assert response.status_code == 404
        assert "pedido" in response.json()["detail"].lower()
    
    def test_titulo_padrao_quando_vazio(self, client: TestClient, pedido_valido: str):
        """Regra: Se titulo_comentario não for fornecido, usar 'Sem Titulo'"""
        response = client.post(
            "/avaliacao_pedidos/",
            json={
                "id_pedido": pedido_valido,
                "avaliacao": 4
            }
        )
        assert response.status_code == 201
        data = response.json()
        assert data["titulo_comentario"] == "Sem Titulo"
    
    def test_comentario_padrao_quando_vazio(self, client: TestClient, pedido_valido: str):
        """Regra: Se comentario não for fornecido, usar 'Sem Comentário'"""
        response = client.post(
            "/avaliacao_pedidos/",
            json={
                "id_pedido": pedido_valido,
                "avaliacao": 3
            }
        )
        assert response.status_code == 201
        data = response.json()
        assert data["comentario"] == "Sem Comentário"
    
    def test_ambos_padroes_quando_vazios(self, client: TestClient, pedido_valido: str):
        """Validar que ambos os padrões são aplicados quando vazios"""
        response = client.post(
            "/avaliacao_pedidos/",
            json={
                "id_pedido": pedido_valido,
                "avaliacao": 2
            }
        )
        assert response.status_code == 201
        data = response.json()
        assert data["titulo_comentario"] == "Sem Titulo"
        assert data["comentario"] == "Sem Comentário"
    
    def test_listar_avaliacoes(self, client: TestClient, pedido_valido: str):
        """Validar listagem de todas as avaliações"""
        # Criar várias avaliações
        for i in range(1, 4):
            client.post(
                "/avaliacao_pedidos/",
                json={
                    "id_pedido": pedido_valido,
                    "avaliacao": i,
                    "titulo_comentario": f"Avaliação {i}",
                    "comentario": f"Comentário {i}"
                }
            )
        
        response = client.get("/avaliacao_pedidos/")
        assert response.status_code == 200
        assert len(response.json()) == 3
    
    def test_buscar_avaliacao_por_id(self, client: TestClient, pedido_valido: str):
        """Validar busca de avaliação pelo ID"""
        # Criar avaliação
        create_response = client.post(
            "/avaliacao_pedidos/",
            json={
                "id_pedido": pedido_valido,
                "avaliacao": 5,
                "titulo_comentario": "Ótimo",
                "comentario": "Muito bom mesmo"
            }
        )
        avaliacao_id = create_response.json()["id_avaliacao"]
        
        # Buscar avaliação
        response = client.get(f"/avaliacao_pedidos/{avaliacao_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id_avaliacao"] == avaliacao_id
        assert data["id_pedido"] == pedido_valido
    
    def test_buscar_avaliacao_inexistente(self, client: TestClient):
        """Validar erro ao buscar avaliação que não existe"""
        response = client.get("/avaliacao_pedidos/avaliacao_inexistente")
        assert response.status_code == 404
        assert "não encontrada" in response.json()["detail"].lower()
    
    def test_atualizar_avaliacao(self, client: TestClient, pedido_valido: str):
        """Validar atualização de dados da avaliação"""
        # Criar avaliação
        create_response = client.post(
            "/avaliacao_pedidos/",
            json={
                "id_pedido": pedido_valido,
                "avaliacao": 3,
                "titulo_comentario": "Razoável",
                "comentario": "Poderia ser melhor"
            }
        )
        avaliacao_id = create_response.json()["id_avaliacao"]
        
        # Atualizar
        update_response = client.patch(
            f"/avaliacao_pedidos/{avaliacao_id}",
            json={
                "avaliacao": 4,
                "titulo_comentario": "Bom",
                "comentario": "Melhor que imaginava"
            }
        )
        assert update_response.status_code == 200
        data = update_response.json()
        assert data["avaliacao"] == 4
        assert data["titulo_comentario"] == "Bom"
    
    def test_atualizar_avaliacao_inexistente(self, client: TestClient):
        """Validar erro ao tentar atualizar avaliação que não existe"""
        response = client.patch(
            "/avaliacao_pedidos/avaliacao_inexistente",
            json={"avaliacao": 5}
        )
        assert response.status_code == 404
        assert "não encontrada" in response.json()["detail"].lower()
    
    def test_deletar_avaliacao(self, client: TestClient, pedido_valido: str):
        """Validar deleção de avaliação"""
        # Criar avaliação
        create_response = client.post(
            "/avaliacao_pedidos/",
            json={
                "id_pedido": pedido_valido,
                "avaliacao": 5,
                "titulo_comentario": "Perfeito",
                "comentario": "Sem defeitos"
            }
        )
        avaliacao_id = create_response.json()["id_avaliacao"]
        
        # Deletar avaliação
        delete_response = client.delete(f"/avaliacao_pedidos/{avaliacao_id}")
        assert delete_response.status_code == 204
        
        # Validar que foi deletado
        response = client.get(f"/avaliacao_pedidos/{avaliacao_id}")
        assert response.status_code == 404
    
    def test_validacao_avaliacao_minima(self, client: TestClient, pedido_valido: str):
        """Validar que avaliação mínima é 1"""
        response = client.post(
            "/avaliacao_pedidos/",
            json={
                "id_pedido": pedido_valido,
                "avaliacao": 0  # Inválido
            }
        )
        assert response.status_code == 422
    
    def test_validacao_avaliacao_maxima(self, client: TestClient, pedido_valido: str):
        """Validar que avaliação máxima é 5"""
        response = client.post(
            "/avaliacao_pedidos/",
            json={
                "id_pedido": pedido_valido,
                "avaliacao": 6  # Inválido
            }
        )
        assert response.status_code == 422
    
    def test_todas_avaliacoes_validas(self, client: TestClient, pedido_valido: str):
        """Validar que todas as avaliações de 1 a 5 são aceitas"""
        for nota in range(1, 6):
            response = client.post(
                "/avaliacao_pedidos/",
                json={
                    "id_pedido": pedido_valido,
                    "avaliacao": nota,
                    "titulo_comentario": f"Nota {nota}",
                    "comentario": f"Avaliação com nota {nota}"
                }
            )
            assert response.status_code == 201, f"Avaliação {nota} não foi aceita"
            data = response.json()
            assert data["avaliacao"] == nota
    
    def test_validacao_titulo_max_length(self, client: TestClient, pedido_valido: str):
        """Validar que titulo deve ter no máximo 255 caracteres"""
        response = client.post(
            "/avaliacao_pedidos/",
            json={
                "id_pedido": pedido_valido,
                "avaliacao": 5,
                "titulo_comentario": "a" * 256  # Inválido
            }
        )
        assert response.status_code == 422
    
    def test_validacao_comentario_max_length(self, client: TestClient, pedido_valido: str):
        """Validar que comentário deve ter no máximo 1000 caracteres"""
        response = client.post(
            "/avaliacao_pedidos/",
            json={
                "id_pedido": pedido_valido,
                "avaliacao": 5,
                "comentario": "a" * 1001  # Inválido
            }
        )
        assert response.status_code == 422
    
    def test_multiplas_avaliacoes_mesmo_pedido(self, client: TestClient, pedido_valido: str):
        """Validar que um pedido pode ter múltiplas avaliações"""
        # Criar múltiplas avaliações
        avaliacoes_ids = []
        for i in range(1, 4):
            response = client.post(
                "/avaliacao_pedidos/",
                json={
                    "id_pedido": pedido_valido,
                    "avaliacao": i,
                    "titulo_comentario": f"Título {i}",
                    "comentario": f"Comentário {i}"
                }
            )
            assert response.status_code == 201
            avaliacoes_ids.append(response.json()["id_avaliacao"])
        
        # Validar que pode buscar cada uma
        for avaliacao_id in avaliacoes_ids:
            response = client.get(f"/avaliacao_pedidos/{avaliacao_id}")
            assert response.status_code == 200
