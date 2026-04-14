import React from 'react';
import { Card } from '../atoms/Card';
import { Badge } from '../atoms/Badge';

interface ProductCardProps {
  id: string;
  nome: string;
  categoria: string;
  imagem?: string;
  media?: number;
  totalAvaliacoes?: number;
  onView?: (id: string) => void;
}

export const ProductCard: React.FC<ProductCardProps> = ({
  id,
  nome,
  categoria,
  imagem,
  media = 0,
  totalAvaliacoes = 0,
  onView,
}) => {
  const renderStars = (rating: number) => {
    return (
      <div className="flex gap-1">
        {[1, 2, 3, 4, 5].map((star) => (
          <svg
            key={star}
            className={`w-4 h-4 ${star <= Math.round(rating) ? 'text-yellow-500' : 'text-primary-600'}`}
            fill="currentColor"
            viewBox="0 0 20 20"
          >
            <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
          </svg>
        ))}
      </div>
    );
  };

  return (
    <Card className="overflow-hidden flex flex-col h-full hover:shadow-2xl transition-all duration-300 hover:-translate-y-1 border border-primary-700 hover:border-secondary-500">
      {/* Imagem do Produto com Badge de Categoria */}
      <div className="relative w-full bg-gradient-to-br from-gray-100 to-gray-200 overflow-hidden" style={{ aspectRatio: '1/1' }}>
        {/* Badge de Categoria */}
        <div className="absolute top-3 right-3 z-20">
          <Badge variant="secondary" className="text-xs font-bold shadow-lg">
            {categoria}
          </Badge>
        </div>

        {/* Imagem */}
        <img
          src={imagem || 'https://via.placeholder.com/300x300/e5e7eb/9ca3af?text=Sem+Imagem'}
          alt={nome}
          className="w-full h-full object-cover hover:scale-125 transition-transform duration-500 cursor-pointer"
          onError={(e) => {
            (e.target as HTMLImageElement).src = 'https://via.placeholder.com/300x300/e5e7eb/9ca3af?text=Sem+Imagem';
          }}
        />

        {/* Overlay no hover */}
        <div className="absolute inset-0 bg-black/0 hover:bg-black/10 transition-colors duration-300" />
      </div>

      {/* Informações do Produto */}
      <div className="p-5 flex-1 flex flex-col gap-4">
        {/* Nome do Produto */}
        <div className="flex-1">
          <h3 className="text-lg font-bold text-primary-50 line-clamp-2 hover:text-secondary-500 transition-colors">
            {nome}
          </h3>
        </div>

        {/* Avaliações */}
        {(media > 0 || totalAvaliacoes > 0) && (
          <div className="border-t border-primary-700 pt-3">
            <div className="flex items-center gap-2 mb-2">
              {renderStars(media)}
            </div>
            <p className="text-xs text-primary-400 font-semibold">
              <span className="text-yellow-400 font-bold">{media.toFixed(1)}</span> / <span className="text-primary-300">5</span>
              <span className="text-primary-500 ml-2">({totalAvaliacoes})</span>
            </p>
          </div>
        )}
      </div>

      {/* Botões de Ação */}
      <div className="border-t border-primary-700 p-4 grid grid-cols-3 gap-2 bg-gradient-to-r from-primary-800 to-primary-700 hover:from-primary-700 hover:to-primary-600 transition-all duration-300">
        {onView && (
          <button
            onClick={() => onView(id)}
            className="px-2 py-2 bg-gradient-to-br from-secondary-600 to-secondary-700 text-white text-xs font-bold rounded hover:from-secondary-500 hover:to-secondary-600 transition-all shadow-md hover:shadow-lg transform hover:scale-105 "
            title="Ver detalhes"
          >
            👁️ Ver
          </button>
        )}
      </div>
    </Card>
  );
};
