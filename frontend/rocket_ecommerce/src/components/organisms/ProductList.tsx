import React, { useRef, useEffect } from 'react';
import { ProductCard } from '../molecules/ProductCard';
import { LoadingSpinner } from '../atoms/LoadingSpinner';
import { ErrorMessage } from '../atoms/ErrorMessage';
import { Button } from '../atoms/Button';

interface Produto {
  id_produto: string;
  nome_produto: string;
  categoria_produto: string;
  link_imagem?: string;
  peso_produto_gramas?: number;
  comprimento_centimetros?: number;
  altura_centimetros?: number;
  largura_centimetros?: number;
  media?: number;
  total_avaliacoes?: number;
}

interface ProductListProps {
  products: Produto[];
  isLoading: boolean;
  hasMore: boolean;
  error?: string;
  onLoadMore: () => void;
  onView?: (id: string) => void;
}

export const ProductList: React.FC<ProductListProps> = ({
  products,
  isLoading,
  hasMore,
  error,
  onLoadMore,
  onView,
}) => {
  const observerTarget = useRef<HTMLDivElement>(null);

  // Intersection Observer for infinite scroll
  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        if (entries[0].isIntersecting && hasMore && !isLoading) {
          onLoadMore();
        }
      },
      { threshold: 0.1 }
    );

    if (observerTarget.current) {
      observer.observe(observerTarget.current);
    }

    return () => observer.disconnect();
  }, [hasMore, isLoading, onLoadMore]);

  if (products.length === 0 && !isLoading) {
    return (
      <div className="container-max py-12 text-center">
        <p className="text-primary-400">Nenhum produto encontrado.</p>
      </div>
    );
  }

  return (
    <div className="container-max py-8">
      {error && <ErrorMessage message={error} />}

      <div className="grid grid-cols-responsive gap-responsive">
        {products.map((product) => (
          <ProductCard
            key={product.id_produto}
            id={product.id_produto}
            nome={product.nome_produto}
            categoria={product.categoria_produto}
            imagem={product.link_imagem}
            media={product.media || 0}
            totalAvaliacoes={product.total_avaliacoes || 0}
            onView={onView}
          />
        ))}
      </div>

      {isLoading && (
        <div className="flex justify-center py-12">
          <LoadingSpinner size="lg" />
        </div>
      )}

      {hasMore && !isLoading && (
        <div className="flex justify-center mt-8 mb-8">
          <Button onClick={onLoadMore} variant="secondary">
            Carregar mais produtos
          </Button>
        </div>
      )}

      <div ref={observerTarget} className="h-4" />
    </div>
  );
};
