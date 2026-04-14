import { useEffect, useState } from 'react';
import type { Produto, PaginatedResponse } from '../services/produtoService';
import { produtoService } from '../services/produtoService';
import { ProdutoCard } from './ProdutoCard';
import { ProdutoDetalhe } from './ProdutoDetalhe';
import { SearchBar } from './SearchBar';

export function ProdutoLista() {
  const [produtos, setProdutos] = useState<Produto[]>([]);
  const [produtoSelecionado, setProdutoSelecionado] = useState<Produto | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [erro, setErro] = useState<string | null>(null);
  const [currentPage, setCurrentPage] = useState(0);
  const [hasMore, setHasMore] = useState(true);
  const LIMIT = 12;

  useEffect(() => {
    carregarProdutos(0, true);
  }, []);

  const carregarProdutos = async (page: number = 0, isNewSearch: boolean = false) => {
    setIsLoading(true);
    setErro(null);
    try {
      const skip = page * LIMIT;
      const resposta: PaginatedResponse = await produtoService.listarProdutos(skip, LIMIT);
      if (isNewSearch) {
        setProdutos(resposta.data);
      } else {
        setProdutos(prev => [...prev, ...resposta.data]);
      }
      setCurrentPage(page + 1);
      setHasMore(resposta.has_next);
    } catch (err) {
      setErro('Erro ao carregar produtos.');
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSearch = async (termo: string) => {
    if (!termo.trim()) {
      setCurrentPage(0);
      setHasMore(true);
      await carregarProdutos(0, true);
      return;
    }

    setIsLoading(true);
    setErro(null);
    try {
      const resultado = await produtoService.buscarProdutosPorNome(termo, 0, LIMIT);
      setProdutos(resultado.data);
      setHasMore(resultado.has_next);
      setCurrentPage(1);
    } catch (err) {
      setErro(`Nenhum produto encontrado.`);
      setProdutos([]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleLoadMore = () => {
    if (!hasMore || isLoading) return;
    carregarProdutos(currentPage, false);
  };

  if (produtoSelecionado) {
    return (
      <ProdutoDetalhe 
        produto={produtoSelecionado} 
        onVoltar={() => setProdutoSelecionado(null)}
      />
    );
  }

  return (
    <div style={{ 
      minHeight: '100vh',
      backgroundColor: '#f5f5f5'
    }}>
      {/* Header */}
      <div style={{
        backgroundColor: 'white',
        borderBottom: '1px solid #e0e0e0',
        padding: '20px 0'
      }}>
        <div style={{ maxWidth: '1200px', margin: '0 auto', padding: '0 20px' }}>
          <h1 style={{
            margin: '0 0 20px 0',
            fontSize: '32px',
            fontWeight: '700',
            color: '#1a1a1a'
          }}>
            🛍️ Catálogo de Produtos
          </h1>
          <SearchBar onSearch={handleSearch} isLoading={isLoading} />
        </div>
      </div>

      {/* Main Content */}
      <div style={{ maxWidth: '1200px', margin: '0 auto', padding: '40px 20px' }}>
        {/* Error Message */}
        {erro && (
          <div style={{ 
            backgroundColor: '#fee', 
            color: '#c33', 
            padding: '16px',
            borderRadius: '8px',
            marginBottom: '20px',
            border: '1px solid #f5a5a5'
          }}>
            <strong>⚠️</strong> {erro}
          </div>
        )}

        {/* Loading State */}
        {isLoading && produtos.length === 0 ? (
          <div style={{
            textAlign: 'center',
            padding: '60px 20px',
            color: '#666'
          }}>
            <div style={{ fontSize: '48px', marginBottom: '16px' }}>⏳</div>
            <p style={{ fontSize: '16px' }}>Carregando produtos...</p>
          </div>
        ) : produtos.length === 0 ? (
          <div style={{
            textAlign: 'center',
            padding: '60px 20px',
            color: '#999'
          }}>
            <div style={{ fontSize: '48px', marginBottom: '16px' }}>📦</div>
            <p style={{ fontSize: '16px' }}>Nenhum produto encontrado.</p>
          </div>
        ) : (
          <>
            {/* Grid de Produtos */}
            <div style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))',
              gap: '24px',
              marginBottom: '40px'
            }}>
              {produtos.map((produto) => (
                <ProdutoCard 
                  key={produto.id_produto}
                  produto={produto}
                  onClick={() => setProdutoSelecionado(produto)}
                />
              ))}
            </div>

            {/* Load More Button */}
            {hasMore && (
              <div style={{ textAlign: 'center', marginTop: '40px' }}>
                <button
                  onClick={handleLoadMore}
                  disabled={isLoading}
                  style={{
                    padding: '12px 32px',
                    fontSize: '16px',
                    fontWeight: '600',
                    backgroundColor: '#667eea',
                    color: 'white',
                    border: 'none',
                    borderRadius: '8px',
                    cursor: isLoading ? 'not-allowed' : 'pointer',
                    opacity: isLoading ? 0.6 : 1,
                    transition: 'all 0.2s'
                  }}
                  onMouseEnter={(e) => {
                    if (!isLoading) (e.target as HTMLButtonElement).style.backgroundColor = '#5568d3';
                  }}
                  onMouseLeave={(e) => {
                    (e.target as HTMLButtonElement).style.backgroundColor = '#667eea';
                  }}
                >
                  {isLoading ? 'Carregando...' : 'Carregar Mais'}
                </button>
              </div>
            )}
          </>
        )}
      </div>
    </div>
  );
}
