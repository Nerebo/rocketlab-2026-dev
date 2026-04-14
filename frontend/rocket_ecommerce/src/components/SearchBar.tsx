import { useState, useRef } from 'react';

interface SearchBarProps {
  onSearch: (termo: string) => void;
  isLoading?: boolean;
}

export function SearchBar({ onSearch, isLoading = false }: SearchBarProps) {
  const [termo, setTermo] = useState('');
  const debounceTimeout = useRef<number | null>(null);

  // Debounce para busca automática
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    setTermo(value);
    if (debounceTimeout.current) clearTimeout(debounceTimeout.current);
    debounceTimeout.current = window.setTimeout(() => {
      onSearch(value);
    }, 500);
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (debounceTimeout.current) clearTimeout(debounceTimeout.current);
    onSearch(termo);
  };

  const handleLimpar = () => {
    setTermo('');
    if (debounceTimeout.current) clearTimeout(debounceTimeout.current);
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
      <div style={{ flex: 1, position: 'relative', display: 'flex' }}>
        <input
          type="text"
          placeholder="🔍 Buscar produtos por nome, categoria..."
          value={termo}
          onChange={handleChange}
          disabled={isLoading}
          style={{
            flex: 1,
            padding: '12px 16px',
            fontSize: '14px',
            border: '1px solid #ddd',
            borderRadius: '6px 0 0 6px',
            outline: 'none',
            transition: 'border-color 0.2s',
            backgroundColor: 'white',
            color: '#1a1a1a'
          }}
          onFocus={(e) => {
            e.currentTarget.style.borderColor = '#667eea';
            e.currentTarget.style.boxShadow = '0 0 0 3px rgba(102, 126, 234, 0.1)';
          }}
          onBlur={(e) => {
            e.currentTarget.style.borderColor = '#ddd';
            e.currentTarget.style.boxShadow = 'none';
          }}
        />
        <button 
          type="submit" 
          disabled={isLoading}
          style={{
            padding: '12px 20px',
            backgroundColor: '#667eea',
            color: 'white',
            border: 'none',
            borderRadius: '0 6px 6px 0',
            cursor: isLoading ? 'not-allowed' : 'pointer',
            fontSize: '14px',
            fontWeight: '600',
            transition: 'background-color 0.2s',
            opacity: isLoading ? 0.6 : 1
          }}
          onMouseEnter={(e) => {
            if (!isLoading) (e.currentTarget as HTMLButtonElement).style.backgroundColor = '#5568d3';
          }}
          onMouseLeave={(e) => {
            (e.currentTarget as HTMLButtonElement).style.backgroundColor = '#667eea';
          }}
        >
          Buscar
        </button>
      </div>
      
      {termo && (
        <button
          type="button"
          onClick={handleLimpar}
          disabled={isLoading}
          style={{
            padding: '12px 16px',
            backgroundColor: '#f0f0f0',
            color: '#666',
            border: '1px solid #ddd',
            borderRadius: '6px',
            cursor: isLoading ? 'not-allowed' : 'pointer',
            fontSize: '14px',
            fontWeight: '600',
            transition: 'all 0.2s',
            opacity: isLoading ? 0.6 : 1
          }}
          onMouseEnter={(e) => {
            if (!isLoading) {
              (e.currentTarget as HTMLButtonElement).style.backgroundColor = '#e0e0e0';
              (e.currentTarget as HTMLButtonElement).style.color = '#1a1a1a';
            }
          }}
          onMouseLeave={(e) => {
            (e.currentTarget as HTMLButtonElement).style.backgroundColor = '#f0f0f0';
            (e.currentTarget as HTMLButtonElement).style.color = '#666';
          }}
        >
          ✕ Limpar
        </button>
      )}
    </form>
  );
}
