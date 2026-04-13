const API_URL = 'http://localhost:8000/produtos';

export interface Produto {
  id_produto: string;
  nome_produto: string;
  peso_produto_gramas: number;
  comprimento_centimetros: number;
  altura_centimetros: number;
  largura_centimetros: number;
  categoria_produto: string;
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

export const produtoService = {
  async listarProdutos(skip: number = 0, limit: number = 100): Promise<PaginatedResponse> {
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
        throw new Error(`Erro ao buscar produto: ${response.statusText}`);
      }
      return await response.json();
    } catch (error) {
      console.error(`Erro ao buscar produto ${id}:`, error);
      throw error;
    }
  },

  async buscarProdutosPorNome(nome: string): Promise<Produto[]> {
    try {
      const response = await fetch(`${API_URL}/buscar/${encodeURIComponent(nome)}`);
      if (!response.ok) {
        throw new Error(`Erro ao buscar produtos: ${response.statusText}`);
      }
      return await response.json();
    } catch (error) {
      console.error(`Erro ao buscar produtos com nome ${nome}:`, error);
      throw error;
    }
  },
};
