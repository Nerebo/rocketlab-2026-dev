import React, { useEffect, useState } from 'react';
import { Card } from '../atoms/Card';
import { Button } from '../atoms/Button';
import { LoadingSpinner } from '../atoms/LoadingSpinner';
import { ErrorMessage } from '../atoms/ErrorMessage';
import { ReviewCard } from '../molecules/ReviewCard';
import { RatingDisplay } from '../molecules/RatingDisplay';

interface Produto {
  id_produto: string;
  nome_produto: string;
  categoria_produto: string;
  link_imagem?: string;
  peso_produto_gramas?: number;
  comprimento_centimetros?: number;
  altura_centimetros?: number;
  largura_centimetros?: number;
  preco_medio?: number;
  numero_vendas?: number;
}

interface Review {
  id_avaliacao: string;
  avaliacao: number;
  titulo_comentario?: string;
  comentario?: string;
  data_comentario?: string;
}

interface MediaAvaliacao {
  media: number;
  total: number;
  breakdown: Record<number, number>;
}

interface ProductDetailProps {
  product: Produto;
  isLoading: boolean;
  error?: string;
  onClose: () => void;
  onEdit?: (id: string) => void;
  onDelete?: (id: string) => void;
  fetchReviews?: (productId: string) => Promise<Review[]>;
  fetchRatingStats?: (productId: string) => Promise<MediaAvaliacao>;
}

export const ProductDetail: React.FC<ProductDetailProps> = ({
  product,
  isLoading,
  error,
  onClose,
  onEdit,
  onDelete,
  fetchReviews,
  fetchRatingStats,
}) => {
  const [reviews, setReviews] = useState<Review[]>([]);
  const [ratingStats, setRatingStats] = useState<MediaAvaliacao | null>(null);
  const [reviewsLoading, setReviewsLoading] = useState(false);

  useEffect(() => {
    const loadReviews = async () => {
      if (!fetchReviews || !fetchRatingStats) return;

      setReviewsLoading(true);

      try {
        const [reviewsData, statsData] = await Promise.all([
          fetchReviews(product.id_produto),
          fetchRatingStats(product.id_produto),
        ]);

        setReviews(reviewsData);
        setRatingStats(statsData);
      } catch (err) {
        // Silently fail - show empty state instead
        console.error('Erro ao carregar avaliações:', err);
      } finally {
        setReviewsLoading(false);
      }
    };

    loadReviews();
  }, [product.id_produto, fetchReviews, fetchRatingStats]);

  if (isLoading) {
    return (
      <div className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 z-50">
        <LoadingSpinner size="lg" fullscreen={false} />
      </div>
    );
  }

  return (
    <div className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-60 z-50 p-4 backdrop-blur-sm">
      <Card className="w-full max-w-5xl max-h-[90vh] overflow-hidden flex flex-col bg-gradient-to-b from-primary-750 to-primary-800 shadow-2xl rounded-3xl border border-primary-600">
        {/* HEADER */}
        <div className="border-b border-primary-600 bg-gradient-to-r from-primary-800 to-primary-750 px-8 py-6 flex items-start justify-between gap-6">
          <div className="flex-1">
            <span className="inline-flex px-4 py-2 bg-gradient-to-r from-secondary-500 to-secondary-600 text-white text-xs font-bold uppercase rounded-full mb-4 border border-secondary-400 shadow-lg">
              {product.categoria_produto}
            </span>
            <h1 className="text-4xl font-bold text-primary-50 mb-1 leading-tight">{product.nome_produto}</h1>
            <p className="text-primary-300 text-sm font-medium">Produto #{product.id_produto.slice(0, 8)}</p>
          </div>
          <button
            onClick={onClose}
            className="text-primary-400 hover:text-primary-100 transition-colors p-2 hover:bg-primary-700 rounded-full flex-shrink-0"
            title="Fechar"
          >
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        {/* CONTENT */}
        <div className="flex-1 overflow-y-auto">
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 p-8">
            {/* COLUNA ESQUERDA - IMAGEM */}
            <div className="col-span-1 flex justify-center lg:justify-start">
              <div className="w-full max-w-sm bg-gradient-to-br from-primary-700 via-primary-750 to-primary-800 rounded-2xl overflow-hidden shadow-xl border border-primary-600 hover:border-primary-500 transition-all" style={{ aspectRatio: '1/1' }}>
                <img
                  src={product.link_imagem || 'https://via.placeholder.com/500x500/e5e7eb/9ca3af?text=Sem+Imagem'}
                  alt={product.nome_produto}
                  className="w-full h-full object-cover hover:scale-105 transition-transform duration-500"
                  onError={(e) => {
                    (e.target as HTMLImageElement).src = 'https://via.placeholder.com/500x500/e5e7eb/9ca3af?text=Sem+Imagem';
                  }}
                />
              </div>
            </div>

            {/* COLUNA DIREITA - DETALHES */}
            <div className="col-span-1 lg:col-span-2 flex flex-col gap-5">
              {error && <ErrorMessage message={error} />}

              {/* CARD PRINCIPAL - Preço e Vendas com Avaliações */}
              <div className="p-6 bg-gradient-to-br from-primary-700 to-primary-800 rounded-2xl border border-primary-600 shadow-lg hover:border-primary-500 transition-all">
                <div className="grid grid-cols-2 gap-4 mb-6">
                  {product.preco_medio !== undefined && product.preco_medio !== null && (
                    <div className="bg-primary-800/50 backdrop-blur-sm rounded-lg p-4 border border-primary-600/50 hover:border-primary-500/70 transition-colors">
                      <p className="text-primary-300 text-xs font-semibold uppercase tracking-wide mb-1">💰 Preço Médio</p>
                      <p className="text-primary-50 text-3xl font-bold">R$ {product.preco_medio.toFixed(2)}</p>
                    </div>
                  )}
                  {product.numero_vendas !== undefined && product.numero_vendas !== null && (
                    <div className="bg-primary-800/50 backdrop-blur-sm rounded-lg p-4 border border-primary-600/50 hover:border-primary-500/70 transition-colors">
                      <p className="text-primary-300 text-xs font-semibold uppercase tracking-wide mb-1">📊 Vendas</p>
                      <p className="text-primary-50 text-3xl font-bold">{product.numero_vendas}</p>
                    </div>
                  )}
                </div>

                {/* Rating na mesma seção */}
                {ratingStats && (
                  <div className="flex items-center gap-4 pt-4 border-t border-primary-600/50">
                    <div className="flex flex-col items-center">
                      <RatingDisplay rating={ratingStats.media} size="lg" />
                      <p className="text-primary-300 text-xs mt-1 font-semibold">{ratingStats.total} avaliações</p>
                    </div>
                    <div className="flex-1 space-y-2">
                      {[5, 4, 3, 2, 1].map((star) => (
                        <div key={star} className="flex items-center gap-2">
                          <span className="text-xs font-bold text-primary-300 w-6">{star}⭐</span>
                          <div className="h-1.5 bg-primary-600/50 rounded-full flex-1 overflow-hidden">
                            <div
                              className="h-full bg-gradient-to-r from-yellow-400 to-yellow-300 rounded-full transition-all duration-300"
                              style={{
                                width: `${ratingStats.total > 0 ? (ratingStats.breakdown[star] / ratingStats.total) * 100 : 0}%`,
                              }}
                            />
                          </div>
                          <span className="text-xs font-bold text-primary-300 w-6 text-right">{ratingStats.breakdown[star]}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>

              {/* ESPECIFICAÇÕES */}
              {(product.peso_produto_gramas || product.comprimento_centimetros || product.altura_centimetros || product.largura_centimetros) && (
                <div className="p-6 bg-gradient-to-br from-primary-700 to-primary-800 rounded-2xl border border-primary-600 hover:border-primary-500 transition-all">
                  <h3 className="text-lg font-bold text-primary-50 mb-4 flex items-center gap-2">
                    <span className="text-2xl">📦</span>
                    Dimensões e Peso
                  </h3>
                  <div className="grid grid-cols-2 gap-3">
                    {product.peso_produto_gramas && (
                      <div className="bg-primary-800/50 rounded-lg p-4 border border-primary-600/50 hover:border-primary-500/70 transition-colors">
                        <p className="text-primary-300 text-xs font-semibold uppercase tracking-wide mb-2">⚖️ Peso</p>
                        <p className="text-primary-50 font-bold text-lg">{product.peso_produto_gramas.toLocaleString('pt-BR')}g</p>
                      </div>
                    )}
                    {product.comprimento_centimetros && (
                      <div className="bg-primary-800/50 rounded-lg p-4 border border-primary-600/50 hover:border-primary-500/70 transition-colors">
                        <p className="text-primary-300 text-xs font-semibold uppercase tracking-wide mb-2">📏 Comprimento</p>
                        <p className="text-primary-50 font-bold text-lg">{product.comprimento_centimetros.toLocaleString('pt-BR')} cm</p>
                      </div>
                    )}
                    {product.altura_centimetros && (
                      <div className="bg-primary-800/50 rounded-lg p-4 border border-primary-600/50 hover:border-primary-500/70 transition-colors">
                        <p className="text-primary-300 text-xs font-semibold uppercase tracking-wide mb-2">📐 Altura</p>
                        <p className="text-primary-50 font-bold text-lg">{product.altura_centimetros.toLocaleString('pt-BR')} cm</p>
                      </div>
                    )}
                    {product.largura_centimetros && (
                      <div className="bg-primary-800/50 rounded-lg p-4 border border-primary-600/50 hover:border-primary-500/70 transition-colors">
                        <p className="text-primary-300 text-xs font-semibold uppercase tracking-wide mb-2">↔️ Largura</p>
                        <p className="text-primary-50 font-bold text-lg">{product.largura_centimetros.toLocaleString('pt-BR')} cm</p>
                      </div>
                    )}
                  </div>
                </div>
              )}

              {/* AVALIAÇÕES / COMENTÁRIOS */}
              {reviewsLoading ? (
                <div className="flex justify-center py-8">
                  <LoadingSpinner />
                </div>
              ) : reviews.length > 0 ? (
                <div className="p-6 bg-gradient-to-br from-primary-700 to-primary-800 rounded-2xl border border-primary-600">
                  <h3 className="text-lg font-bold text-primary-50 mb-4 flex items-center gap-2">
                    <span className="text-2xl">💬</span>
                    {reviews.length} {reviews.length === 1 ? 'Comentário' : 'Comentários'}
                  </h3>
                  <div className="space-y-2 max-h-64 overflow-y-auto pr-2">
                    {reviews.map((review) => (
                      <div key={review.id_avaliacao} className="bg-primary-800/50 p-4 rounded-lg border border-primary-600/50 hover:border-primary-500/70 transition-colors">
                        <ReviewCard
                          titulo={review.titulo_comentario || ''}
                          comentario={review.comentario || ''}
                          rating={review.avaliacao}
                          data={review.data_comentario || ''}
                        />
                      </div>
                    ))}
                  </div>
                </div>
              ) : null}
            </div>
          </div>
        </div>

        {/* FOOTER */}
        <div className="border-t border-primary-600 bg-gradient-to-r from-primary-800 to-primary-750 px-8 py-5 flex gap-3 justify-end">
          {onEdit && (
            <Button
              onClick={() => onEdit(product.id_produto)}
              variant="secondary"
              className="px-6 py-2.5 font-semibold text-sm flex items-center gap-2"
            >
              ✏️ Editar
            </Button>
          )}
          {onDelete && (
            <Button
              onClick={() => onDelete(product.id_produto)}
              variant="danger"
              className="px-6 py-2.5 font-semibold text-sm flex items-center gap-2"
            >
              🗑️ Deletar
            </Button>
          )}
          <Button onClick={onClose} variant="primary" className="px-8 py-2.5 font-semibold text-sm">
            ← Fechar
          </Button>
        </div>
      </Card>
    </div>
  );
};
