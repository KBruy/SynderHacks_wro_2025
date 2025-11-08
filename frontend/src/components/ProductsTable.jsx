export default function ProductsTable({ products, selectedProduct, onSelectProduct, onShowDetails }) {
  return (
    <table className="products-table">
      <thead>
        <tr>
          <th>SKU</th>
          <th>Nazwa produktu</th>
          <th>Cena</th>
          <th>Nakład</th>
          <th>Status</th>
          <th>Kanał</th>
          <th>Aktywne promocje</th>
        </tr>
      </thead>
      <tbody>
        {products.map((product) => (
          <tr
            key={product.id}
            className={selectedProduct?.id === product.id ? 'selected' : ''}
            onClick={() => onSelectProduct(product)}
          >
            <td>{product.sku}</td>
            <td>
              <span
                className="product-name-link"
                onClick={(e) => {
                  e.stopPropagation();
                  onShowDetails(product);
                }}
              >
                {product.name}
              </span>
            </td>
            <td>{product.price.toFixed(2)} PLN</td>
            <td>
              <span className={`stock-indicator ${product.stock < 20 ? 'low' : ''}`}>
                {product.stock} szt.
              </span>
            </td>
            <td>
              <span className={`status-badge ${product.status}`}>
                {product.status === 'active' ? 'Aktywny' : 'Niski stan'}
              </span>
            </td>
            <td>
              <span className={`channel-badge ${product.channel}`}>
                {product.channel}
              </span>
            </td>
            <td>
              {product.active_promotions && product.active_promotions.length > 0 ? (
                <div className="active-promotions">
                  {product.active_promotions.map((promo) => (
                    <span key={promo.id} className={`promo-badge ${promo.type}`} title={promo.description}>
                      {promo.type === 'price' && '💰'}
                      {promo.type === 'promo' && '🎉'}
                      {promo.type === 'bundle' && '📦'}
                      {' '}
                      {promo.type}
                    </span>
                  ))}
                </div>
              ) : (
                <span className="no-promo">-</span>
              )}
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
