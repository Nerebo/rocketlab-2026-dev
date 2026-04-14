const API_URL = 'http://localhost:8000/produtos';

export interface Produto {
  id_produto: string;
  nome_produto: string;
  peso_produto_gramas?: number;
  comprimento_centimetros?: number;
  altura_centimetros?: number;
  largura_centimetros?: number;
  categoria_produto: string;
  link_imagem?: string;
  media?: number;
  media_avaliacao?: number;
  total_avaliacoes?: number;
}

export interface PaginatedResponse {
  data: Produto[];
  total: number;
  skip: number;
  limit: number;
  total_pages: number;
  current_page: number;
  has_next: boolean;
  has_prev: boolean;
}

export interface Avaliacao {
  id_avaliacao: string;
  id_pedido: string;
  avaliacao: number;
  titulo_comentario?: string;
  comentario?: string;
  data_comentario?: string;
  data_resposta?: string;
}

export interface MediaAvaliacao {
  id_produto: string;
  media: number;
  total: number;
  breakdown: {
    [key: number]: number;
  };
}

export const produtoService = {
  async listarProdutos(skip: number = 0, limit: number = 12): Promise<PaginatedResponse> {
    try {
      const response = await fetch(`${API_URL}/?skip=${skip}&limit=${limit}`);
      if (!response.ok) {
        throw new Error(`Erro ao buscar produtos: ${response.statusText}`);
      }
      return await response.json();
    } catch (error) {
      console.error('Erro na requisição de produtos:', error);
      throw error;
    }
  },

  async obterProdutoPorId(id: string): Promise<Produto> {
    try {
      const response = await fetch(`${API_URL}/${id}`);
      if (!response.ok) {
        throw new Error(`Erro ao buscar produto: Nenhum produto com o ID ${id} encontrado`);
      }
      return await response.json();
    } catch (error) {
      throw error;
    }
  },

  async buscarProdutosPorNome(nome: string, skip: number = 0, limit: number = 12): Promise<PaginatedResponse> {
    try {
      const response = await fetch(`${API_URL}/buscar/${encodeURIComponent(nome)}?skip=${skip}&limit=${limit}`);
      if (!response.ok) {
        throw new Error(`Erro ao buscar produtos: Nenhum produto com o nome ${nome} encontrado`);
      }
      return await response.json();
    } catch (error) {
      throw error;
    }
  },

  async obterAvaliacoesProduto(id: string): Promise<Avaliacao[]> {
    try {
      const response = await fetch(`${API_URL}/${id}/avaliacoes`);
      if (!response.ok) {
        console.warn(`Erro ao buscar avaliações: ${response.statusText}`);
        return [];
      }
      const data = await response.json();
      return Array.isArray(data) ? data : [];
    } catch (error) {
      console.error(`Erro ao buscar avaliações do produto ${id}:`, error);
      return []; // Retorna array vazio em caso de erro
    }
  },

  async obterMediaAvaliacao(id: string): Promise<MediaAvaliacao> {
    try {
      const response = await fetch(`${API_URL}/${id}/media-avaliacao`);
      if (!response.ok) {
        console.warn(`Erro ao buscar média de avaliações: ${response.statusText}`);
        return { id_produto: id, media: 0, total: 0, breakdown: { 1: 0, 2: 0, 3: 0, 4: 0, 5: 0 } };
      }
      return await response.json();
    } catch (error) {
      console.error(`Erro ao buscar média de avaliações do produto ${id}:`, error);
      return { id_produto: id, media: 0, total: 0, breakdown: { 1: 0, 2: 0, 3: 0, 4: 0, 5: 0 } };
    }
  },

  async criarProduto(data: {
    nome_produto: string;
    categoria_produto: string;
    peso_produto_gramas?: number;
    comprimento_centimetros?: number;
    altura_centimetros?: number;
    largura_centimetros?: number;
  }): Promise<Produto> {
    try {
      const response = await fetch(API_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
      });
      if (!response.ok) {
        throw new Error(`Erro ao criar produto: ${response.statusText}`);
      }
      return await response.json();
    } catch (error) {
      console.error('Erro ao criar produto:', error);
      throw error;
    }
  },

  async atualizarProduto(
    id: string,
    data: Partial<{
      nome_produto: string;
      categoria_produto: string;
      peso_produto_gramas?: number;
      comprimento_centimetros?: number;
      altura_centimetros?: number;
      largura_centimetros?: number;
    }>
  ): Promise<Produto> {
    try {
      const response = await fetch(`${API_URL}/${id}`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
      });
      if (!response.ok) {
        throw new Error(`Erro ao atualizar produto: ${response.statusText}`);
      }
      return await response.json();
    } catch (error) {
      console.error(`Erro ao atualizar produto ${id}:`, error);
      throw error;
    }
  },

  async deletarProduto(id: string): Promise<void> {
    try {
      const response = await fetch(`${API_URL}/${id}`, {
        method: 'DELETE',
      });
      if (!response.ok) {
        throw new Error(`Erro ao deletar produto: ${response.statusText}`);
      }
    } catch (error) {
      console.error(`Erro ao deletar produto ${id}:`, error);
      throw error;
    }
  },
};
