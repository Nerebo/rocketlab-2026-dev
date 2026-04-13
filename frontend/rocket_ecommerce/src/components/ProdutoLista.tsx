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

  useEffect(() => {
    carregarProdutos();
  }, []);

  const carregarProdutos = async () => {
    setIsLoading(true);
    setErro(null);
    try {
      const resposta: PaginatedResponse = await produtoService.listarProdutos(0, 100);
      setProdutos(resposta.data);
    } catch (err) {
      setErro('Erro ao carregar produtos.');
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSearch = async (termo: string) => {
    if (!termo.trim()) {
      await carregarProdutos();
      return;
    }

    setIsLoading(true);
    setErro(null);
    try {
      const resultado = await produtoService.buscarProdutosPorNome(termo);
      setProdutos(resultado);
    } catch (err) {
      setErro(`Nenhum produto encontrado.`);
      setProdutos([]);
    } finally {
      setIsLoading(false);
    }
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
    <div style={{ padding: '20px', maxWidth: '800px', margin: '0 auto' }}>
      <h1>Catálogo de Produtos</h1>
      
      <SearchBar onSearch={handleSearch} isLoading={isLoading} />

      {erro && (
        <div style={{ 
          backgroundColor: '#fee', 
          color: '#c33', 
          padding: '10px', 
          borderRadius: '5px',
          marginBottom: '20px'
        }}>
          {erro}
        </div>
      )}

      {isLoading ? (
        <p>Carregando produtos...</p>
      ) : produtos.length === 0 ? (
        <p>Nenhum produto encontrado.</p>
      ) : (
        <div>
          <p>Total: {produtos.length} produto(s)</p>
          <div>
            {produtos.map((produto) => (
              <ProdutoCard
                key={produto.id_produto}
                produto={produto}
                onClick={setProdutoSelecionado}
              />
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
