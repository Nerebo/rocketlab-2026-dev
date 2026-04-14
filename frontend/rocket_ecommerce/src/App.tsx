import { useState, useCallback, useEffect } from 'react';
import { SearchBar } from './components/molecules';
import { ProductList, ProductDetail, ProductForm } from './components/organisms';
import { Button, ErrorMessage } from './components/atoms';
import { produtoService, type Produto, type Avaliacao, type MediaAvaliacao } from './services/produtoService';

interface ProdutoComAvaliacoes extends Produto {
  media?: number;
  total_avaliacoes?: number;
}

function App() {
  // State management
  const [produtos, setProdutos] = useState<ProdutoComAvaliacoes[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [isSearching, setIsSearching] = useState(false);
  const [error, setError] = useState<string>();
  const [currentPage, setCurrentPage] = useState(0);
  const [hasMore, setHasMore] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [isSearchActive, setIsSearchActive] = useState(false);

  // Detail and form modals
  const [selectedProduct, setSelectedProduct] = useState<ProdutoComAvaliacoes | null>(null);
  const [showDetail, setShowDetail] = useState(false);
  const [showForm, setShowForm] = useState(false);
  const [editingProduct, setEditingProduct] = useState<ProdutoComAvaliacoes | null>(null);
  const [formLoading, setFormLoading] = useState(false);

  // Pagination size
  const LIMIT = 12;

  // Load products with pagination
  const loadProducts = useCallback(async (pageNum: number, isNewSearch: boolean = false) => {
    setIsLoading(true);
    setError(undefined);

    try {
      const skip = pageNum * LIMIT;
      const result = await produtoService.listarProdutos(skip, LIMIT);

      if (isNewSearch) {
        setProdutos(result.data);
      } else {
        setProdutos((prev) => [...prev, ...result.data]);
      }

      setCurrentPage(pageNum + 1);
      setHasMore(result.has_next);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erro ao carregar produtos');
    } finally {
      setIsLoading(false);
    }
  }, []);

  // Search for products
  const handleSearch = useCallback(async (term: string, pageNum: number = 0) => {
    setSearchTerm(term);
    if (pageNum === 0) setCurrentPage(0);

    if (!term.trim()) {
      setIsSearchActive(false);
      await loadProducts(0, true);
      return;
    }

    setIsSearchActive(true);
    if (pageNum === 0) setIsSearching(true);
    if (pageNum === 0) setError(undefined);

    try {
      const skip = pageNum * LIMIT;
      const results = await produtoService.buscarProdutosPorNome(term, skip, LIMIT);
      
      if (pageNum === 0) {
        setProdutos(results.data);
      } else {
        setProdutos((prev) => [...prev, ...results.data]);
      }
      
      setCurrentPage(pageNum + 1);
      setHasMore(results.has_next);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erro ao buscar produtos');
      if (pageNum === 0) {
        setProdutos([]);
      }
    } finally {
      if (pageNum === 0) setIsSearching(false);
    }
  }, [LIMIT]);

  // Load more products
  const handleLoadMore = useCallback(() => {
    if (isSearchActive) {
      // Carregar mais resultados da busca
      handleSearch(searchTerm, currentPage);
    } else {
      // Carregar mais produtos da lista geral
      loadProducts(currentPage);
    }
  }, [currentPage, isSearchActive, searchTerm, handleSearch, loadProducts]);

  // View product detail
  const handleViewProduct = useCallback((id: string) => {
    const product = produtos.find((p) => p.id_produto === id);
    if (product) {
      setSelectedProduct(product);
      setEditingProduct(null);
      setShowDetail(true);
    }
  }, [produtos]);

  // Edit product
  const handleEditProduct = useCallback((id: string) => {
    const product = produtos.find((p) => p.id_produto === id);
    if (product) {
      setEditingProduct(product);
      setSelectedProduct(null);
      setShowDetail(false);
      setShowForm(true);
    }
  }, [produtos]);

  // Delete product
  const handleDeleteProduct = useCallback(
    async (id: string) => {
      if (!window.confirm('Tem certeza que deseja deletar este produto?')) return;

      setFormLoading(true);
      try {
        await produtoService.deletarProduto(id);
        setProdutos((prev) => prev.filter((p) => p.id_produto !== id));
        setShowDetail(false);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Erro ao deletar produto');
      } finally {
        setFormLoading(false);
      }
    },
    []
  );

  // Handle form submit for create/update
  const handleFormSubmit = useCallback(
    async (data: {
      nome_produto: string;
      categoria_produto: string;
      peso_produto_gramas?: number;
      comprimento_centimetros?: number;
      altura_centimetros?: number;
      largura_centimetros?: number;
    }) => {
      setFormLoading(true);
      try {
        if (editingProduct) {
          await produtoService.atualizarProduto(editingProduct.id_produto, data);
        } else {
          await produtoService.criarProduto(data);
        }

        // Refresh the list
        setProdutos([]);
        setCurrentPage(0);
        await loadProducts(0, true);

        setShowForm(false);
        setEditingProduct(null);
      } catch (err) {
        throw err;
      } finally {
        setFormLoading(false);
      }
    },
    [editingProduct, loadProducts]
  );

  // Fetch reviews for detail view
  const fetchProductReviews = useCallback(async (productId: string): Promise<Avaliacao[]> => {
    return produtoService.obterAvaliacoesProduto(productId);
  }, []);

  // Fetch rating stats for detail view
  const fetchRatingStats = useCallback(async (productId: string): Promise<MediaAvaliacao> => {
    return produtoService.obterMediaAvaliacao(productId);
  }, []);

  // Initial load
  useEffect(() => {
    loadProducts(0, true);
  }, [loadProducts]);

  return (
    <div className="bg-primary-900 min-h-screen">
      {/* Header */}
      <header className="bg-primary-800 border-b border-primary-700 sticky top-0 z-40">
        <div className="container-max py-6">
          <div className="flex items-center justify-between gap-4 mb-6">
            <h1 className="text-3xl font-serif">🚀 RocketLab Marketplace</h1>
            <Button onClick={() => setShowForm(true)} variant="primary">
              ➕ Novo Produto
            </Button>
          </div>
          <SearchBar onSearch={handleSearch} isLoading={isSearching} />
        </div>
      </header>

      {/* Main content */}
      <main>
        {error && (
          <div className="container-max mt-6">
            <ErrorMessage message={error} onDismiss={() => setError(undefined)} />
          </div>
        )}

        <ProductList
          products={produtos}
          isLoading={isLoading && currentPage === 0}
          hasMore={hasMore}
          onLoadMore={handleLoadMore}
          onView={handleViewProduct}
        />
      </main>

      {/* Modals */}
      {showDetail && selectedProduct && (
        <ProductDetail
          product={selectedProduct}
          isLoading={false}
          onClose={() => setShowDetail(false)}
          onEdit={handleEditProduct}
          onDelete={handleDeleteProduct}
          fetchReviews={fetchProductReviews}
          fetchRatingStats={fetchRatingStats}
        />
      )}

      <ProductForm
        isOpen={showForm}
        onClose={() => {
          setShowForm(false);
          setEditingProduct(null);
        }}
        onSubmit={handleFormSubmit}
        initialData={editingProduct || undefined}
        isLoading={formLoading}
      />
    </div>
  );
}

export default App;