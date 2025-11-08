import { useState, useEffect } from 'react';
import { api } from '../services/api';

export default function ConnectionsPanel({ onConnectionChange }) {
  const [connections, setConnections] = useState([]);
  const [loading, setLoading] = useState(false);
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({
    name: '',
    platform: 'woocommerce',
    store_url: '',
    api_key: '',
    api_secret: ''
  });
  const [formError, setFormError] = useState(null);
  const [syncing, setSyncing] = useState(null);

  useEffect(() => {
    loadConnections();
  }, []);

  const loadConnections = async () => {
    setLoading(true);
    try {
      const data = await api.getConnections();
      setConnections(data);
    } catch (err) {
      console.error('Failed to load connections:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setFormError(null);

    try {
      await api.createConnection(formData);
      setShowForm(false);
      setFormData({
        name: '',
        platform: 'woocommerce',
        store_url: '',
        api_key: '',
        api_secret: ''
      });
      await loadConnections();
      if (onConnectionChange) onConnectionChange();
    } catch (err) {
      setFormError(err.message);
    }
  };

  const handleDelete = async (id) => {
    if (!confirm('Czy na pewno chcesz usunąć to połączenie?')) return;

    try {
      await api.deleteConnection(id);
      await loadConnections();
      if (onConnectionChange) onConnectionChange();
    } catch (err) {
      alert('Błąd usuwania połączenia: ' + err.message);
    }
  };

  const handleSync = async (id) => {
    setSyncing(id);
    try {
      const result = await api.syncConnection(id);
      alert(result.message);
      await loadConnections();
      if (onConnectionChange) onConnectionChange();
    } catch (err) {
      alert('Błąd synchronizacji: ' + err.message);
    } finally {
      setSyncing(null);
    }
  };

  const handleQuickDemo = async () => {
    if (!confirm('Utworzyć demo sklepy do testów? (WooCommerce + Shopify)')) return;

    setLoading(true);
    try {
      const result = await api.quickDemoSetup();
      alert(result.message + '\n\nTeraz możesz kliknąć "Synchronizuj" aby pobrać przykładowe produkty!');
      await loadConnections();
      if (onConnectionChange) onConnectionChange();
    } catch (err) {
      alert('Błąd tworzenia demo sklepów: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="connections-panel">
      <div className="panel-header">
        <h2>Połączenia ze sklepami</h2>
        <div style={{ display: 'flex', gap: '10px' }}>
          <button className="btn-demo" onClick={handleQuickDemo} disabled={loading}>
            🎮 Szybkie Demo
          </button>
          <button className="btn-primary" onClick={() => setShowForm(!showForm)}>
            {showForm ? 'Anuluj' : '+ Dodaj połączenie'}
          </button>
        </div>
      </div>

      {showForm && (
        <form className="connection-form" onSubmit={handleSubmit}>
          <div className="form-group">
            <label>Nazwa połączenia</label>
            <input
              type="text"
              value={formData.name}
              onChange={(e) => setFormData({...formData, name: e.target.value})}
              placeholder="np. Mój sklep WooCommerce"
              required
            />
          </div>

          <div className="form-group">
            <label>Platforma</label>
            <select
              value={formData.platform}
              onChange={(e) => setFormData({...formData, platform: e.target.value})}
            >
              <option value="woocommerce">WooCommerce</option>
              <option value="shopify">Shopify</option>
            </select>
          </div>

          <div className="form-group">
            <label>URL sklepu</label>
            <input
              type="url"
              value={formData.store_url}
              onChange={(e) => setFormData({...formData, store_url: e.target.value})}
              placeholder={formData.platform === 'shopify' ? 'myshop.myshopify.com' : 'https://myshop.com'}
              required
            />
            <small>
              {formData.platform === 'shopify'
                ? 'Format: myshop.myshopify.com (bez https://)'
                : 'Pełny URL sklepu'
              }
            </small>
          </div>

          <div className="form-group">
            <label>
              {formData.platform === 'shopify' ? 'Access Token' : 'Consumer Key'}
            </label>
            <input
              type="text"
              value={formData.api_key}
              onChange={(e) => setFormData({...formData, api_key: e.target.value})}
              placeholder="API Key"
              required
            />
          </div>

          {formData.platform === 'woocommerce' && (
            <div className="form-group">
              <label>Consumer Secret</label>
              <input
                type="password"
                value={formData.api_secret}
                onChange={(e) => setFormData({...formData, api_secret: e.target.value})}
                placeholder="API Secret"
                required
              />
            </div>
          )}

          {formError && <div className="error">{formError}</div>}

          <button type="submit" className="btn-primary">Dodaj i przetestuj połączenie</button>
        </form>
      )}

      {loading ? (
        <div className="loading">Ładowanie połączeń</div>
      ) : connections.length === 0 ? (
        <div className="empty-state">Brak połączeń. Dodaj pierwszy sklep!</div>
      ) : (
        <div className="connections-list">
          {connections.map((conn) => (
            <div key={conn.id} className="connection-card">
              <div className="connection-header">
                <div>
                  <h3>{conn.name}</h3>
                  <span className={`platform-badge ${conn.platform}`}>
                    {conn.platform}
                  </span>
                </div>
                <span className={`status-indicator ${conn.is_active ? 'active' : 'inactive'}`}>
                  {conn.is_active ? 'Aktywne' : 'Nieaktywne'}
                </span>
              </div>

              <div className="connection-info">
                <div><strong>URL:</strong> {conn.store_url}</div>
                {conn.last_sync && (
                  <div><strong>Ostatnia sync:</strong> {new Date(conn.last_sync).toLocaleString('pl-PL')}</div>
                )}
              </div>

              <div className="connection-actions">
                <button
                  className="btn-secondary"
                  onClick={() => handleSync(conn.id)}
                  disabled={!conn.is_active || syncing === conn.id}
                >
                  {syncing === conn.id ? 'Synchronizacja...' : 'Synchronizuj'}
                </button>
                <button
                  className="btn-danger"
                  onClick={() => handleDelete(conn.id)}
                >
                  Usuń
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
