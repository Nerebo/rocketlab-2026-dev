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
      <Card className="w-full max-w-7xl max-h-[95vh] overflow-hidden flex flex-col bg-primary-800 shadow-2xl rounded-2xl border border-primary-700">
        <div className="flex-1 overflow-y-auto">
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 p-6 lg:p-10">
            {/* COLUNA ESQUERDA - IMAGEM GRANDE */}
            <div className="col-span-1 flex flex-col justify-start sticky top-0 lg:top-auto">
              <div className="bg-gradient-to-br from-primary-700 to-primary-800 rounded-2xl overflow-hidden shadow-lg border border-primary-600" style={{ aspectRatio: '1/1' }}>
                <img
                  src={product.link_imagem || 'https://via.placeholder.com/500x500/e5e7eb/9ca3af?text=Sem+Imagem'}
                  alt={product.nome_produto}
                  className="w-full h-full object-cover hover:scale-110 transition-transform duration-500"
                  onError={(e) => {
                    (e.target as HTMLImageElement).src = 'https://via.placeholder.com/500x500/e5e7eb/9ca3af?text=Sem+Imagem';
                  }}
                />
              </div>
            </div>

            {/* COLUNA DIREITA - CONTEÚDO */}
            <div className="col-span-1 lg:col-span-2 flex flex-col gap-6 overflow-y-auto pr-2 max-h-[calc(95vh-80px)]">
              {/* Header com botão fechar */}
              <div className="flex items-start justify-between gap-4 pb-6 border-b-2 border-primary-700">
                <div className="flex-1">
                  <span className="inline-block px-4 py-1.5 bg-gradient-to-r from-secondary-600 to-secondary-700 text-white text-xs font-bold uppercase rounded-full mb-3 border border-secondary-500">
                    {product.categoria_produto}
                  </span>
                  <h1 className="text-3xl lg:text-4xl font-bold text-primary-50 mb-2 leading-tight">{product.nome_produto}</h1>
                </div>
                <button
                  onClick={onClose}
                  className="text-primary-400 hover:text-primary-200 transition-colors flex-shrink-0 p-2 hover:bg-primary-700 rounded-lg"
                  title="Fechar"
                >
                  <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </div>

              {error && <ErrorMessage message={error} />}

              {/* Especificações */}
              {(product.peso_produto_gramas || product.comprimento_centimetros || product.altura_centimetros || product.largura_centimetros) && (
                <div className="p-6 bg-gradient-to-br from-primary-700 to-primary-800 rounded-xl border border-primary-600 hover:border-primary-500 transition-colors">
                  <h3 className="text-lg font-bold text-primary-50 mb-4 flex items-center gap-2">
                    <span className="text-2xl">📦</span>
                    Especificações do Produto
                  </h3>
                  <div className="grid grid-cols-2 gap-4">
                    {product.peso_produto_gramas && (
                      <div className="flex items-start gap-3 p-3 bg-primary-800 rounded-lg border border-primary-600">
                        <span className="text-2xl">⚖️</span>
                        <div>
                          <p className="text-primary-300 font-semibold text-sm">Peso</p>
                          <p className="text-primary-50 font-bold text-base">{product.peso_produto_gramas}g</p>
                        </div>
                      </div>
                    )}
                    {product.comprimento_centimetros && (
                      <div className="flex items-start gap-3 p-3 bg-primary-800 rounded-lg border border-primary-600">
                        <span className="text-2xl">📏</span>
                        <div>
                          <p className="text-primary-300 font-semibold text-sm">Comprimento</p>
                          <p className="text-primary-50 font-bold text-base">{product.comprimento_centimetros}cm</p>
                        </div>
                      </div>
                    )}
                    {product.altura_centimetros && (
                      <div className="flex items-start gap-3 p-3 bg-primary-800 rounded-lg border border-primary-600">
                        <span className="text-2xl">📐</span>
                        <div>
                          <p className="text-primary-300 font-semibold text-sm">Altura</p>
                          <p className="text-primary-50 font-bold text-base">{product.altura_centimetros}cm</p>
                        </div>
                      </div>
                    )}
                    {product.largura_centimetros && (
                      <div className="flex items-start gap-3 p-3 bg-primary-800 rounded-lg border border-primary-600">
                        <span className="text-2xl">↔️</span>
                        <div>
                          <p className="text-primary-300 font-semibold text-sm">Largura</p>
                          <p className="text-primary-50 font-bold text-base">{product.largura_centimetros}cm</p>
                        </div>
                      </div>
                    )}
                  </div>
                </div>
              )}

              {/* Média de Avaliações */}
              {ratingStats && (
                <div className="p-6 bg-gradient-to-br from-primary-700 to-primary-800 rounded-xl border border-primary-600">
                  <h3 className="text-lg font-bold text-primary-50 mb-4 flex items-center gap-2">
                    <span className="text-2xl">⭐</span>
                    Avaliações dos Clientes
                  </h3>
                  <div className="flex items-center gap-6">
                    <div className="flex flex-col items-center min-w-max">
                      <RatingDisplay rating={ratingStats.media} size="lg" />
                      <p className="text-primary-200 text-sm mt-2 font-bold">{ratingStats.total} {ratingStats.total === 1 ? 'avaliação' : 'avaliações'}</p>
                    </div>
                    <div className="flex-1 space-y-3">
                      {[5, 4, 3, 2, 1].map((star) => (
                        <div key={star} className="flex items-center gap-2">
                          <span className="text-sm font-bold text-primary-200 w-10">{star}⭐</span>
                          <div className="h-2.5 bg-primary-600 rounded-full flex-1 overflow-hidden shadow-inner">
                            <div
                              className="h-full bg-gradient-to-r from-yellow-400 to-yellow-500 rounded-full transition-all duration-500"
                              style={{
                                width: `${ratingStats.total > 0 ? (ratingStats.breakdown[star] / ratingStats.total) * 100 : 0}%`,
                              }}
                            />
                          </div>
                          <span className="text-sm font-bold text-primary-200 w-10 text-right">{ratingStats.breakdown[star]}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              )}

              {/* Comentários das Avaliações */}
              {reviewsLoading ? (
                <div className="flex justify-center py-8">
                  <LoadingSpinner />
                </div>
              ) : reviews.length > 0 ? (
                <div className="p-6 bg-primary-700 rounded-xl border border-primary-600">
                  <h3 className="text-lg font-bold text-primary-50 mb-4 flex items-center gap-2">
                    <span className="text-2xl">💬</span>
                    Comentários de Clientes ({reviews.length})
                  </h3>
                  <div className="space-y-3 max-h-80 overflow-y-auto pr-3">
                    {reviews.map((review) => (
                      <div key={review.id_avaliacao} className="p-3 bg-primary-800 rounded-lg border border-primary-600 hover:border-primary-500 transition-colors">
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

        {/* Botão Fechar na Parte Inferior */}
        <div className="border-t-2 border-primary-700 bg-gradient-to-r from-primary-800 to-primary-700 p-6 flex gap-3 justify-end shadow-sm">
          {onEdit && (
            <Button
              onClick={() => onEdit(product.id_produto)}
              variant="secondary"
              className="px-6 py-3 font-semibold flex items-center gap-2"
            >
              ✏️ Editar
            </Button>
          )}
          {onDelete && (
            <Button
              onClick={() => onDelete(product.id_produto)}
              variant="danger"
              className="px-6 py-3 font-semibold flex items-center gap-2"
            >
              🗑️ Deletar
            </Button>
          )}
          <Button onClick={onClose} variant="secondary" className="px-8 py-3 font-semibold">
            ← Fechar
          </Button>
        </div>
      </Card>
    </div>
  );
};
