import type { Produto } from '../services/produtoService';

interface ProdutoCardProps {
  produto: Produto;
  onClick: (produto: Produto) => void;
}

export function ProdutoCard({ produto, onClick }: ProdutoCardProps) {
  const imagemPadrao = 'https://via.placeholder.com/300x200/e0e0e0/999?text=Sem+Imagem';
  const media = produto.media || produto.media_avaliacao || 0;
  const totalAvaliacoes = produto.total_avaliacoes || 0;

  return (
    <div
      onClick={() => onClick(produto)}
      style={{
        backgroundColor: 'white',
        borderRadius: '8px',
        boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
        overflow: 'hidden',
        cursor: 'pointer',
        transition: 'all 0.3s ease',
        height: '100%',
        display: 'flex',
        flexDirection: 'column'
      }}
      onMouseEnter={(e) => {
        const el = e.currentTarget;
        el.style.boxShadow = '0 8px 16px rgba(0,0,0,0.15)';
        el.style.transform = 'translateY(-4px)';
      }}
      onMouseLeave={(e) => {
        const el = e.currentTarget;
        el.style.boxShadow = '0 2px 8px rgba(0,0,0,0.1)';
        el.style.transform = 'translateY(0)';
      }}
    >
      {/* Imagem do Produto */}
      <div style={{
        width: '100%',
        height: '200px',
        backgroundColor: '#f5f5f5',
        overflow: 'hidden',
        position: 'relative'
      }}>
        <img 
          src={produto.link_imagem || imagemPadrao}
          alt={produto.nome_produto}
          style={{
            width: '100%',
            height: '100%',
            objectFit: 'cover',
            transition: 'transform 0.3s ease'
          }}
          onError={(e) => {
            const img = e.target as HTMLImageElement;
            img.src = imagemPadrao;
          }}
        />
        {/* Badge de Categoria */}
        <div style={{
          position: 'absolute',
          top: '8px',
          right: '8px',
          backgroundColor: '#667eea',
          color: 'white',
          padding: '4px 12px',
          borderRadius: '20px',
          fontSize: '12px',
          fontWeight: '600',
          zIndex: 1
        }}>
          {produto.categoria_produto}
        </div>
      </div>

      {/* Conteúdo */}
      <div style={{ padding: '16px', flex: 1, display: 'flex', flexDirection: 'column' }}>
        <h3 style={{
          margin: '0 0 8px 0',
          fontSize: '16px',
          fontWeight: '600',
          color: '#1a1a1a',
          overflow: 'hidden',
          textOverflow: 'ellipsis',
          whiteSpace: 'nowrap'
        }}>
          {produto.nome_produto}
        </h3>

        {/* Rating */}
        <div style={{
          display: 'flex',
          alignItems: 'center',
          gap: '8px',
          marginBottom: '12px',
          fontSize: '14px'
        }}>
          <div style={{
            display: 'flex',
            gap: '2px',
            color: '#ffc107'
          }}>
            {'⭐'.repeat(Math.floor(media))}
            {media % 1 !== 0 && '⭐'}
          </div>
          <span style={{ color: '#666' }}>
            {media > 0 ? `${media.toFixed(1)}` : 'Sem avaliações'}
            {totalAvaliacoes > 0 && ` (${totalAvaliacoes})`}
          </span>
        </div>

        {/* Dimensões */}
        {(produto.peso_produto_gramas || produto.comprimento_centimetros) && (
          <div style={{
            fontSize: '12px',
            color: '#888',
            marginTop: 'auto',
            paddingTop: '8px',
            borderTop: '1px solid #f0f0f0'
          }}>
            {produto.peso_produto_gramas && (
              <div>{produto.peso_produto_gramas}g</div>
            )}
            {produto.comprimento_centimetros && (
              <div>{produto.comprimento_centimetros}cm x {produto.altura_centimetros}cm x {produto.largura_centimetros}cm</div>
            )}
          </div>
        )}
      </div>

      {/* CTA */}
      <div style={{
        padding: '12px 16px',
        backgroundColor: '#f8f8f8',
        borderTop: '1px solid #f0f0f0',
        textAlign: 'center'
      }}>
        <button
          onClick={(e) => {
            e.stopPropagation();
            onClick(produto);
          }}
          style={{
            width: '100%',
            padding: '10px',
            backgroundColor: '#667eea',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            cursor: 'pointer',
            fontSize: '14px',
            fontWeight: '600',
            transition: 'background-color 0.2s'
          }}
          onMouseEnter={(e) => {
            const btn = e.target as HTMLButtonElement;
            btn.style.backgroundColor = '#5568d3';
          }}
          onMouseLeave={(e) => {
            const btn = e.target as HTMLButtonElement;
            btn.style.backgroundColor = '#667eea';
          }}
        >
          Ver Detalhes
        </button>
      </div>
    </div>
  );
}
