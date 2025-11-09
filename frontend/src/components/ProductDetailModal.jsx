import { useState, useEffect } from 'react';
import { api } from '../services/api';

export default function ProductDetailModal({ product, onClose }) {
  const [details, setDetails] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const loadDetails = async () => {
      setLoading(true);
      setError(null);
      try {
        const data = await api.getProductDetails(product.id);
        setDetails(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    if (product) {
      loadDetails();
    }
  }, [product]);

  const formatDate = (dateString) => {
    if (!dateString) return 'N/A';
    const date = new Date(dateString.replace(' ', 'T'));
    return date.toLocaleString('pl-PL', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  const formatExactDate = (dateString) => {
    if (!dateString) return 'N/A';
    const date = new Date(dateString.replace(' ', 'T'));

    return date.toLocaleString('pl-PL', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit',
    });
  };

  if (!product) return null;

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h2>Szczegóły produktu</h2>
          <button className="modal-close" onClick={onClose}>×</button>
        </div>

        {loading && <div className="loading">Ładowanie szczegółów</div>}

        {error && <div className="error">Błąd: {error}</div>}

        {!loading && !error && details && (
          <div className="modal-body">
            {/* Basic Info */}
            <div className="detail-section">
              <h3>Podstawowe informacje</h3>
              <div className="detail-grid">
                <div className="detail-item">
                  <span className="detail-label">SKU:</span>
                  <span className="detail-value">{details.sku}</span>
                </div>
                <div className="detail-item">
                  <span className="detail-label">Nazwa:</span>
                  <span className="detail-value">{details.name}</span>
                </div>
                <div className="detail-item">
                  <span className="detail-label">Cena:</span>
                  <span className="detail-value">{details.price.toFixed(2)} PLN</span>
                </div>
                <div className="detail-item">
                  <span className="detail-label">Nakład:</span>
                  <span className={`detail-value ${details.stock < 20 ? 'low-stock' : ''}`}>
                    {details.stock} szt.
                  </span>
                </div>
                <div className="detail-item">
                  <span className="detail-label">Status:</span>
                  <span className={`status-badge ${details.status}`}>
                    {details.status === 'active' ? 'Aktywny' : 'Niski stan'}
                  </span>
                </div>
                <div className="detail-item">
                  <span className="detail-label">Kanał:</span>
                  <span className={`channel-badge ${details.channel}`}>
                    {details.channel}
                  </span>
                </div>
                <div className="detail-item">
                  <span className="detail-label">Utworzono:</span>
                  <span className="detail-value">{formatDate(details.created_at)}</span>
                </div>
                <div className="detail-item">
                  <span className="detail-label">Zaktualizowano:</span>
                  <span className="detail-value">{formatDate(details.updated_at)}</span>
                </div>
              </div>
            </div>

            {/* Applied Suggestions */}
            {details.applied_suggestions && details.applied_suggestions.length > 0 && (
              <div className="detail-section">
                <h3>Zastosowane sugestie ({details.applied_suggestions.length})</h3>
                <div className="suggestions-list">
                  {details.applied_suggestions.map((sug) => (
                    <div key={sug.id} className="suggestion-item">
                      <span className={`promo-badge ${sug.type}`}>
                        {sug.type === 'price' && '💰'}
                        {sug.type === 'promo' && '🎉'}
                        {sug.type === 'bundle' && '📦'}
                        {' '}
                        {sug.type}
                      </span>
                      <span className="suggestion-desc">{sug.description}</span>
                      <span className="suggestion-time">{formatExactDate(sug.applied_at)}</span>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Event History */}
            {details.event_history && details.event_history.length > 0 && (
              <div className="detail-section">
                <h3>Historia zmian ({details.event_history.length})</h3>
                <div className="history-list">
                  {details.event_history.map((event) => (
                    <div key={event.id} className="history-item">
                      <div className="history-time">{formatExactDate(event.created_at)}</div>
                      <div className="history-desc">{event.description}</div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {(!details.event_history || details.event_history.length === 0) && (
              <div className="detail-section">
                <h3>Historia zmian</h3>
                <div className="empty-state">Brak historii dla tego produktu</div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
