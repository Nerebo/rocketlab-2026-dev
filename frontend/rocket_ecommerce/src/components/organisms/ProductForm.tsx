import React, { useState, useEffect } from 'react';
import { Modal } from '../atoms/Modal';
import { Input } from '../atoms/Input';
import { Button } from '../atoms/Button';
import { ErrorMessage } from '../atoms/ErrorMessage';

interface ProdutoFormData {
  nome_produto: string;
  categoria_produto: string;
  peso_produto_gramas?: number;
  comprimento_centimetros?: number;
  altura_centimetros?: number;
  largura_centimetros?: number;
  media_avaliacao?: number;

}

interface ProductFormProps {
  isOpen: boolean;
  onClose: () => void;
  onSubmit: (data: ProdutoFormData) => Promise<void>;
  initialData?: ProdutoFormData & { id_produto?: string };
  isLoading?: boolean;
}

export const ProductForm: React.FC<ProductFormProps> = ({
  isOpen,
  onClose,
  onSubmit,
  initialData,
  isLoading = false,
}) => {
  const [formData, setFormData] = useState<ProdutoFormData>({
    nome_produto: '',
    categoria_produto: '',
    peso_produto_gramas: undefined,
    comprimento_centimetros: undefined,
    altura_centimetros: undefined,
    largura_centimetros: undefined,
    media_avaliacao: undefined,
  });

  const [errors, setErrors] = useState<Partial<ProdutoFormData>>({});
  const [submitError, setSubmitError] = useState<string>();

  useEffect(() => {
    if (initialData) {
      setFormData({
        nome_produto: initialData.nome_produto,
        categoria_produto: initialData.categoria_produto,
        peso_produto_gramas: initialData.peso_produto_gramas,
        comprimento_centimetros: initialData.comprimento_centimetros,
        altura_centimetros: initialData.altura_centimetros,
        largura_centimetros: initialData.largura_centimetros,
        media_avaliacao: initialData.media_avaliacao,
      });
    } else {
      setFormData({
        nome_produto: '',
        categoria_produto: '',
      });
    }
    setErrors({});
    setSubmitError(undefined);
  }, [initialData, isOpen]);

  const validateForm = (): boolean => {
    const newErrors: Partial<ProdutoFormData> = {};

    if (!formData.nome_produto.trim()) {
      newErrors.nome_produto = 'Nome é obrigatório';
    }
    if (!formData.categoria_produto.trim()) {
      newErrors.categoria_produto = 'Categoria é obrigatória';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!validateForm()) return;

    try {
      setSubmitError(undefined);
      await onSubmit(formData);
      onClose();
    } catch (err) {
      setSubmitError(
        err instanceof Error ? err.message : 'Erro ao salvar produto'
      );
    }
  };

  return (
    <Modal
      isOpen={isOpen}
      onClose={onClose}
      title={initialData ? 'Editar Produto' : 'Novo Produto'}
      size="lg"
    >
      <form onSubmit={handleSubmit} className="space-y-4">
        {submitError && <ErrorMessage message={submitError} />}

        <Input
          label="Nome do Produto"
          required
          value={formData.nome_produto}
          onChange={(e) =>
            setFormData({ ...formData, nome_produto: e.target.value })
          }
          error={errors.nome_produto as string}
          placeholder="Ex: Notebook Dell XPS"
        />

        <Input
          label="Categoria"
          required
          value={formData.categoria_produto}
          onChange={(e) =>
            setFormData({ ...formData, categoria_produto: e.target.value })
          }
          error={errors.categoria_produto as string}
          placeholder="Ex: Eletrônicos"
        />

        <div className="grid grid-cols-2 gap-4">
          <Input
            label="Peso (gramas)"
            type="number"
            value={formData.peso_produto_gramas || ''}
            onChange={(e) =>
              setFormData({
                ...formData,
                peso_produto_gramas: e.target.value ? parseFloat(e.target.value) : undefined,
              })
            }
            placeholder="Ex: 1500"
          />

          <Input
            label="Comprimento (cm)"
            type="number"
            value={formData.comprimento_centimetros || ''}
            onChange={(e) =>
              setFormData({
                ...formData,
                comprimento_centimetros: e.target.value ? parseFloat(e.target.value) : undefined,
              })
            }
            placeholder="Ex: 30"
          />

          <Input
            label="Altura (cm)"
            type="number"
            value={formData.altura_centimetros || ''}
            onChange={(e) =>
              setFormData({
                ...formData,
                altura_centimetros: e.target.value ? parseFloat(e.target.value) : undefined,
              })
            }
            placeholder="Ex: 20"
          />

          <Input
            label="Largura (cm)"
            type="number"
            value={formData.largura_centimetros || ''}
            onChange={(e) =>
              setFormData({
                ...formData,
                largura_centimetros: e.target.value ? parseFloat(e.target.value) : undefined,
              })
            }
            placeholder="Ex: 15"
          />
        </div>

        <div className="flex gap-3 pt-4">
          <Button
            type="button"
            variant="secondary"
            onClick={onClose}
            className="flex-1"
          >
            Cancelar
          </Button>
          <Button
            type="submit"
            variant="primary"
            isLoading={isLoading}
            className="flex-1"
          >
            {initialData ? 'Atualizar' : 'Criar'}
          </Button>
        </div>
      </form>
    </Modal>
  );
};
