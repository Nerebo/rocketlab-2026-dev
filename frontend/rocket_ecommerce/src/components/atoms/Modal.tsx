import React from 'react';

interface ModalProps {
  isOpen: boolean;
  onClose: () => void;
  title?: string;
  children: React.ReactNode;
  actions?: React.ReactNode;
  size?: 'sm' | 'md' | 'lg';
}

export const Modal: React.FC<ModalProps> = ({
  isOpen,
  onClose,
  title,
  children,
  actions,
  size = 'md',
}) => {
  if (!isOpen) return null;

  const sizeClasses = {
    sm: 'max-w-sm',
    md: 'max-w-md',
    lg: 'max-w-lg',
  };

  return (
    <div className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 z-50">
      <div className={`bg-primary-800 rounded-lg border border-primary-700 shadow-2xl ${sizeClasses[size]} w-full mx-4 animate-fade-in`}>
        {title && (
          <div className="flex items-center justify-between p-6 border-b border-primary-700">
            <h2 className="text-2xl font-serif">{title}</h2>
            <button
              onClick={onClose}
              className="text-primary-400 hover:text-primary-200 transition-colors"
            >
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
        )}
        <div className="p-6">
          {children}
        </div>
        {actions && (
          <div className="flex gap-3 p-6 border-t border-primary-700 justify-end">
            {actions}
          </div>
        )}
      </div>
    </div>
  );
};
