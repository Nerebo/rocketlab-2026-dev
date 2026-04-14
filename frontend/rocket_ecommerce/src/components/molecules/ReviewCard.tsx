import React from 'react';
import { Card } from '../atoms/Card';
import { RatingDisplay } from './RatingDisplay';

interface ReviewCardProps {
  titulo: string;
  comentario: string;
  rating: number;
  data: string;
}

export const ReviewCard: React.FC<ReviewCardProps> = ({
  titulo,
  comentario,
  rating,
  data,
}) => {
  const formatDate = (dateString: string) => {
    try {
      const date = new Date(dateString);
      return date.toLocaleDateString('pt-BR', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
      });
    } catch {
      return dateString;
    }
  };

  return (
    <Card className="p-4">
      <div className="flex items-start justify-between gap-4 mb-3">
        <div className="flex-1">
          <RatingDisplay rating={rating} size="sm" />
          {titulo && (
            <h4 className="text-primary-50 font-semibold mt-2">
              {titulo}
            </h4>
          )}
        </div>
        <time className="text-xs text-primary-400 whitespace-nowrap">
          {formatDate(data)}
        </time>
      </div>
      {comentario && (
        <p className="text-primary-200 text-sm leading-relaxed">
          {comentario}
        </p>
      )}
    </Card>
  );
};
