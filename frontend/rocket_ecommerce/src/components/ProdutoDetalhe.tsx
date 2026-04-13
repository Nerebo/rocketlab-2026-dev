import type { Produto } from '../services/produtoService';

interface ProdutoDetalheProps {
  produto: Produto;
  onVoltar: () => void;
}

export function ProdutoDetalhe({ produto, onVoltar }: ProdutoDetalheProps) {

  return (
    <div style={{ padding: '20px', maxWidth: '600px', margin: '0 auto' }}>
      <button
        onClick={onVoltar}
        style={{
          padding: '10px 20px',
          backgroundColor: '#667eea',
          color: 'white',
          border: 'none',
          borderRadius: '5px',
          cursor: 'pointer',
          marginBottom: '20px',
          fontSize: '14px'
        }}
      >
        ← Voltar
      </button>

      <div style={{ backgroundColor: '#f9f9f9', padding: '20px', borderRadius: '5px' }}>
        <h1 style={{ marginTop: 0 }}>{produto.nome_produto}</h1>
        
        <div style={{ marginBottom: '20px' }}>
          <strong>Categoria:</strong> {produto.categoria_produto}
        </div>

        <div style={{ marginBottom: '20px' }}>
          <strong>Peso:</strong> {produto.peso_produto_gramas}g
        </div>

        <div style={{ marginBottom: '20px' }}>
          <h3>Dimensões</h3>
          <p><strong>Comprimento:</strong> {produto.comprimento_centimetros} cm</p>
          <p><strong>Altura:</strong> {produto.altura_centimetros} cm</p>
          <p><strong>Largura:</strong> {produto.largura_centimetros} cm</p>
        </div>
      </div>
    </div>
  );
}
