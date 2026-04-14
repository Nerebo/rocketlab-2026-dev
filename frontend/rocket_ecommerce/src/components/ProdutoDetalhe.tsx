import type { Produto } from '../services/produtoService';

interface ProdutoDetalheProps {
  produto: Produto;
  onVoltar: () => void;
}

export function ProdutoDetalhe({ produto, onVoltar }: ProdutoDetalheProps) {
  const imagemPadrao = 'https://via.placeholder.com/600x400/e0e0e0/999?text=Sem+Imagem';
  const media = produto.media || produto.media_avaliacao || 0;
  const totalAvaliacoes = produto.total_avaliacoes || 0;

  return (
    <div style={{ 
      minHeight: '100vh',
      backgroundColor: '#f5f5f5',
      paddingTop: '20px',
      paddingBottom: '40px'
    }}>
      {/* Back Button */}
      <div style={{ maxWidth: '1000px', margin: '0 auto', padding: '0 20px', marginBottom: '20px' }}>
        <button
          onClick={onVoltar}
          style={{
            display: 'flex',
            alignItems: 'center',
            gap: '8px',
            padding: '10px 20px',
            backgroundColor: 'white',
            color: '#667eea',
            border: '1px solid #667eea',
            borderRadius: '6px',
            cursor: 'pointer',
            fontSize: '14px',
            fontWeight: '600',
            transition: 'all 0.2s'
          }}
          onMouseEnter={(e) => {
            const btn = e.target as HTMLButtonElement;
            btn.style.backgroundColor = '#667eea';
            btn.style.color = 'white';
          }}
          onMouseLeave={(e) => {
            const btn = e.target as HTMLButtonElement;
            btn.style.backgroundColor = 'white';
            btn.style.color = '#667eea';
          }}
        >
          ← Voltar ao Catálogo
        </button>
      </div>

      {/* Main Container */}
      <div style={{ maxWidth: '1000px', margin: '0 auto', padding: '0 20px' }}>
        <div style={{
          display: 'grid',
          gridTemplateColumns: '1fr 1fr',
          gap: '40px',
          backgroundColor: 'white',
          borderRadius: '12px',
          padding: '40px',
          boxShadow: '0 2px 12px rgba(0,0,0,0.08)'
        }}>
          {/* Imagem */}
          <div>
            <div style={{
              width: '100%',
              height: '400px',
              backgroundColor: '#f5f5f5',
              borderRadius: '8px',
              overflow: 'hidden',
              marginBottom: '20px'
            }}>
              <img 
                src={produto.link_imagem || imagemPadrao}
                alt={produto.nome_produto}
                style={{
                  width: '100%',
                  height: '100%',
                  objectFit: 'cover'
                }}
                onError={(e) => {
                  const img = e.target as HTMLImageElement;
                  img.src = imagemPadrao;
                }}
              />
            </div>
          </div>

          {/* Informações */}
          <div>
            {/* Categoria Badge */}
            <div style={{
              display: 'inline-block',
              backgroundColor: '#667eea',
              color: 'white',
              padding: '6px 14px',
              borderRadius: '20px',
              fontSize: '12px',
              fontWeight: '600',
              marginBottom: '16px'
            }}>
              {produto.categoria_produto}
            </div>

            {/* Título */}
            <h1 style={{
              margin: '0 0 16px 0',
              fontSize: '32px',
              fontWeight: '700',
              color: '#1a1a1a',
              lineHeight: '1.3'
            }}>
              {produto.nome_produto}
            </h1>

            {/* Rating */}
            <div style={{
              display: 'flex',
              alignItems: 'center',
              gap: '12px',
              marginBottom: '24px',
              paddingBottom: '24px',
              borderBottom: '1px solid #e0e0e0'
            }}>
              <div style={{
                display: 'flex',
                gap: '2px',
                fontSize: '18px',
                color: '#ffc107'
              }}>
                {'⭐'.repeat(Math.floor(media))}
                {media % 1 !== 0 && '⭐'}
              </div>
              <span style={{ 
                fontSize: '16px',
                fontWeight: '600',
                color: '#1a1a1a'
              }}>
                {media > 0 ? `${media.toFixed(1)}` : 'Sem avaliações'}
              </span>
              {totalAvaliacoes > 0 && (
                <span style={{ 
                  fontSize: '14px',
                  color: '#888'
                }}>
                  ({totalAvaliacoes} {totalAvaliacoes === 1 ? 'avaliação' : 'avaliações'})
                </span>
              )}
            </div>

            {/* Especificações */}
            <div style={{ marginBottom: '24px' }}>
              <h3 style={{
                margin: '0 0 16px 0',
                fontSize: '18px',
                fontWeight: '600',
                color: '#1a1a1a'
              }}>
                Especificações
              </h3>

              <div style={{
                display: 'grid',
                gridTemplateColumns: '1fr 1fr',
                gap: '16px'
              }}>
                {produto.peso_produto_gramas && (
                  <div style={{ padding: '12px', backgroundColor: '#f9f9f9', borderRadius: '6px' }}>
                    <p style={{ margin: '0 0 4px 0', fontSize: '12px', color: '#888', fontWeight: '600', textTransform: 'uppercase' }}>
                      Peso
                    </p>
                    <p style={{ margin: 0, fontSize: '16px', fontWeight: '600', color: '#1a1a1a' }}>
                      {produto.peso_produto_gramas}g
                    </p>
                  </div>
                )}
                
                {produto.comprimento_centimetros && (
                  <div style={{ padding: '12px', backgroundColor: '#f9f9f9', borderRadius: '6px' }}>
                    <p style={{ margin: '0 0 4px 0', fontSize: '12px', color: '#888', fontWeight: '600', textTransform: 'uppercase' }}>
                      Comprimento
                    </p>
                    <p style={{ margin: 0, fontSize: '16px', fontWeight: '600', color: '#1a1a1a' }}>
                      {produto.comprimento_centimetros}cm
                    </p>
                  </div>
                )}

                {produto.altura_centimetros && (
                  <div style={{ padding: '12px', backgroundColor: '#f9f9f9', borderRadius: '6px' }}>
                    <p style={{ margin: '0 0 4px 0', fontSize: '12px', color: '#888', fontWeight: '600', textTransform: 'uppercase' }}>
                      Altura
                    </p>
                    <p style={{ margin: 0, fontSize: '16px', fontWeight: '600', color: '#1a1a1a' }}>
                      {produto.altura_centimetros}cm
                    </p>
                  </div>
                )}

                {produto.largura_centimetros && (
                  <div style={{ padding: '12px', backgroundColor: '#f9f9f9', borderRadius: '6px' }}>
                    <p style={{ margin: '0 0 4px 0', fontSize: '12px', color: '#888', fontWeight: '600', textTransform: 'uppercase' }}>
                      Largura
                    </p>
                    <p style={{ margin: 0, fontSize: '16px', fontWeight: '600', color: '#1a1a1a' }}>
                      {produto.largura_centimetros}cm
                    </p>
                  </div>
                )}
              </div>
            </div>

            {/* CTA Buttons */}
            <div style={{
              display: 'grid',
              gridTemplateColumns: '1fr 1fr',
              gap: '12px',
              marginTop: '32px'
            }}>
              <button
                onClick={onVoltar}
                style={{
                  padding: '14px 20px',
                  backgroundColor: '#f0f0f0',
                  color: '#1a1a1a',
                  border: 'none',
                  borderRadius: '6px',
                  cursor: 'pointer',
                  fontSize: '16px',
                  fontWeight: '600',
                  transition: 'background-color 0.2s'
                }}
                onMouseEnter={(e) => {
                  const btn = e.target as HTMLButtonElement;
                  btn.style.backgroundColor = '#e0e0e0';
                }}
                onMouseLeave={(e) => {
                  const btn = e.target as HTMLButtonElement;
                  btn.style.backgroundColor = '#f0f0f0';
                }}
              >
                Voltar
              </button>

              <button
                onClick={() => {}}
                style={{
                  padding: '14px 20px',
                  backgroundColor: '#667eea',
                  color: 'white',
                  border: 'none',
                  borderRadius: '6px',
                  cursor: 'pointer',
                  fontSize: '16px',
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
                🛒 Adicionar ao Carrinho
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
