import { useState } from 'react';

interface SearchBarProps {
  onSearch: (termo: string) => void;
  isLoading?: boolean;
}

export function SearchBar({ onSearch, isLoading = false }: SearchBarProps) {
  const [termo, setTermo] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (termo.trim()) {
      onSearch(termo);
    }
  };

  const handleLimpar = () => {
    setTermo('');
    onSearch('');
  };

  return (
    <form 
      onSubmit={handleSubmit}
      style={{
        display: 'flex',
        gap: '10px',
        marginBottom: '20px'
      }}
    >
      <input
        type="text"
        placeholder="Buscar produtos..."
        value={termo}
        onChange={(e) => setTermo(e.target.value)}
        disabled={isLoading}
        style={{
          flex: 1,
          padding: '10px',
          fontSize: '14px',
          border: '1px solid #ddd',
          borderRadius: '5px'
        }}
      />
      <button 
        type="submit" 
        disabled={isLoading}
        style={{
          padding: '10px 20px',
          backgroundColor: '#667eea',
          color: 'white',
          border: 'none',
          borderRadius: '5px',
          cursor: 'pointer',
          fontSize: '14px'
        }}
      >
        Buscar
      </button>
      {termo && (
        <button
          type="button"
          onClick={handleLimpar}
          disabled={isLoading}
          style={{
            padding: '10px 20px',
            backgroundColor: '#999',
            color: 'white',
            border: 'none',
            borderRadius: '5px',
            cursor: 'pointer',
            fontSize: '14px'
          }}
        >
          Limpar
        </button>
      )}
    </form>
  );
}
