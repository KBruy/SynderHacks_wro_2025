import { useState, useEffect } from 'react';
import { api } from '../services/api';

export default function SuggestionsPanel({ product, onApplied }) {
  const [suggestions, setSuggestions] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [applying, setApplying] = useState(null);

  useEffect(() => {
    if (!product) {
      setSuggestions([]);
      return;
    }

    const loadSuggestions = async () => {
      setLoading(true);
      setError(null);
      try {
        const data = await api.getSuggestions(product.id);
        setSuggestions(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    loadSuggestions();
  }, [product]);

  const handleApply = async (suggestion) => {
    setApplying(suggestion.id);
    try {
      const result = await api.applySuggestion(suggestion.id);

      // Update local state
      setSuggestions(suggestions.map(s =>
        s.id === suggestion.id
          ? { ...s, status: 'applied', applied_at: result.applied_at }
          : s
      ));

      onApplied({
        type: 'success',
        title: 'Sukces!',
        message: result.message,
      });
    } catch (err) {
      onApplied({
        type: 'error',
        title: 'Błąd',
        message: err.message,
      });
    } finally {
      setApplying(null);
    }
  };

  const getSuggestionTypeLabel = (type) => {
    const labels = {
      price: 'Cena',
      promo: 'Promocja',
      bundle: 'Bundle',
    };
    return labels[type] || type;
  };

  if (!product) {
    return (
      <div className="suggestions-panel">
        <h3>Sugestie</h3>
        <div className="empty-state">
          Wybierz produkt, aby zobaczyć sugestie
        </div>
      </div>
    );
  }

  return (
    <div className="suggestions-panel">
      <h3>Sugestie dla: {product.name}</h3>

      {loading && <div className="loading">Ładowanie</div>}

      {error && <div className="error">Błąd: {error}</div>}

      {!loading && !error && suggestions.length === 0 && (
        <div className="empty-state">Brak sugestii dla tego produktu</div>
      )}

      {!loading && !error && suggestions.length > 0 && (
        <div>
          {suggestions.map((suggestion) => (
            <div
              key={suggestion.id}
              className={`suggestion-card ${suggestion.status}`}
            >
              <div className="suggestion-header">
                <span className={`suggestion-badge ${suggestion.type}`}>
                  {getSuggestionTypeLabel(suggestion.type)}
                </span>
                <span className={`suggestion-status ${suggestion.status}`}>
                  {suggestion.status === 'new' ? 'Nowa' : 'Zastosowana'}
                </span>
              </div>

              <div className="suggestion-description">
                {suggestion.description}
              </div>

              {suggestion.status === 'new' && (
                <button
                  className="apply-button"
                  onClick={() => handleApply(suggestion)}
                  disabled={applying === suggestion.id}
                >
                  {applying === suggestion.id ? 'Stosowanie...' : 'Zastosuj sugestię'}
                </button>
              )}

              {suggestion.status === 'applied' && suggestion.applied_at && (
                <div style={{ fontSize: '0.75rem', color: '#999', marginTop: '8px' }}>
                  Zastosowano: {new Date(suggestion.applied_at).toLocaleString('pl-PL')}
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
