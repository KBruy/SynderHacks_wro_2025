import { useState, useEffect } from 'react';
import { api } from './services/api';
import ProductsTable from './components/ProductsTable';
import SuggestionsPanel from './components/SuggestionsPanel';
import HistoryPanel from './components/HistoryPanel';
import ConnectionsPanel from './components/ConnectionsPanel';
import Notification from './components/Notification';
import ProductDetailModal from './components/ProductDetailModal';

function App() {
  const [activeTab, setActiveTab] = useState('products');
  const [products, setProducts] = useState([]);
  const [selectedProduct, setSelectedProduct] = useState(null);
  const [modalProduct, setModalProduct] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [notification, setNotification] = useState(null);
  const [historyRefresh, setHistoryRefresh] = useState(0);
  const [generatingSuggestions, setGeneratingSuggestions] = useState(false);

  useEffect(() => {
    loadProducts();
  }, []);

  const loadProducts = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await api.getProducts();
      setProducts(data);

      // Auto-select first product for demo
      if (data.length > 0 && !selectedProduct) {
        setSelectedProduct(data[0]);
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleProductSelect = (product) => {
    setSelectedProduct(product);
  };

  const handleShowDetails = (product) => {
    setModalProduct(product);
  };

  const handleSuggestionApplied = (notificationData) => {
    setNotification(notificationData);
    // Refresh products to update price and active promotions
    loadProducts();
    // Refresh history when suggestion is applied
    setHistoryRefresh(prev => prev + 1);
  };

  const handleConnectionChange = () => {
    // Reload products when connections change
    loadProducts();
    setHistoryRefresh(prev => prev + 1);
  };

  const handleGenerateSuggestions = async () => {
    setGeneratingSuggestions(true);
    try {
      const result = await api.generateSuggestionsForAll();
      setNotification({
        type: 'success',
        title: 'Sugestie wygenerowane!',
        message: `Przeanalizowano ${result.products_analyzed} produktów i utworzono ${result.total_suggestions_created} sugestii.`,
      });
      // Refresh to show new suggestions
      if (selectedProduct) {
        setSelectedProduct({ ...selectedProduct });
      }
    } catch (err) {
      setNotification({
        type: 'error',
        title: 'Błąd',
        message: `Nie udało się wygenerować sugestii: ${err.message}`,
      });
    } finally {
      setGeneratingSuggestions(false);
    }
  };

  return (
    <div className="app">
      <header className="header">
        <h1>Product Suggestions Manager</h1>
        <p>Zarządzaj produktami i optymalizuj sprzedaż dzięki inteligentnym sugestiom</p>
      </header>

      <div className="tabs">
        <button
          className={`tab ${activeTab === 'products' ? 'active' : ''}`}
          onClick={() => setActiveTab('products')}
        >
          Produkty i Sugestie
        </button>
        <button
          className={`tab ${activeTab === 'connections' ? 'active' : ''}`}
          onClick={() => setActiveTab('connections')}
        >
          Połączenia ze sklepami
        </button>
      </div>

      {activeTab === 'connections' && (
        <ConnectionsPanel onConnectionChange={handleConnectionChange} />
      )}

      {activeTab === 'products' && (
        <>
          <div className="main-content">
            <div className="products-section">
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
                <h2 className="section-title" style={{ margin: 0 }}>Lista produktów</h2>
                {products.length > 0 && (
                  <button
                    className="btn-primary"
                    onClick={handleGenerateSuggestions}
                    disabled={generatingSuggestions}
                    style={{ fontSize: '0.9rem', padding: '0.5rem 1rem' }}
                  >
                    {generatingSuggestions ? '🔄 Generowanie...' : '🤖 Generuj sugestie AI'}
                  </button>
                )}
              </div>

              {loading && <div className="loading">Ładowanie produktów</div>}

              {error && (
                <div className="error">
                  Błąd ładowania produktów: {error}
                </div>
              )}

              {!loading && !error && products.length === 0 && (
                <div className="empty-state">
                  Brak produktów w bazie danych. Dodaj połączenie ze sklepem i zsynchronizuj produkty.
                </div>
              )}

              {!loading && !error && products.length > 0 && (
                <ProductsTable
                  products={products}
                  selectedProduct={selectedProduct}
                  onSelectProduct={handleProductSelect}
                  onShowDetails={handleShowDetails}
                />
              )}
            </div>

            <div className="sidebar">
              <SuggestionsPanel
                product={selectedProduct}
                onApplied={handleSuggestionApplied}
              />
              <HistoryPanel refreshTrigger={historyRefresh} />
            </div>
          </div>
        </>
      )}

      {notification && (
        <Notification
          type={notification.type}
          title={notification.title}
          message={notification.message}
          onClose={() => setNotification(null)}
        />
      )}

      {modalProduct && (
        <ProductDetailModal
          product={modalProduct}
          onClose={() => setModalProduct(null)}
        />
      )}
    </div>
  );
}

export default App;
