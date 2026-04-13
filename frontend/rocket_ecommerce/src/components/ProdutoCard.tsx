import type { Produto } from '../services/produtoService';

interface ProdutoCardProps {
  produto: Produto;
  onClick: (produto: Produto) => void;
}

export function ProdutoCard({ produto, onClick }: ProdutoCardProps) {
  return (
    <div 
      onClick={() => onClick(produto)}
      style={{
        padding: '15px',
        border: '1px solid #ddd',
        borderRadius: '5px',
        cursor: 'pointer',
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        backgroundColor: '#f9f9f9',
        marginBottom: '10px',
        transition: 'background-color 0.2s'
      }}
      onMouseEnter={(e) => e.currentTarget.style.backgroundColor = '#f0f0f0'}
      onMouseLeave={(e) => e.currentTarget.style.backgroundColor = '#f9f9f9'}
    >
      <div>
        <h3 style={{ margin: '0 0 5px 0', fontSize: '16px' }}>
          {produto.nome_produto}
        </h3>
      </div>
      <span 
        style={{
          backgroundColor: '#667eea',
          color: 'white',
          padding: '5px 10px',
          borderRadius: '3px',
          fontSize: '12px',
          whiteSpace: 'nowrap',
          marginLeft: '20px'
        }}
      >
        {produto.categoria_produto}
      </span>
    </div>
  );
}
