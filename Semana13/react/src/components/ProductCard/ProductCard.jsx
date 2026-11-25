import { Link } from 'react-router-dom'
import formatPrice from '../../utils/formatPrice'
import './ProductCard.css'

export default function ProductCard({ product, deleting, disabled, onDelete }) {
  return (
    <article className="product-card">
      {product.image
        ? <img src={product.image} alt={product.name} loading="lazy" />
        : <div className="product-card-empty">Sin imagen</div>}
      <div className="product-card-body">
        <p className="product-card-category" title={product.category.description}>{product.category.name}</p>
        <h2>{product.name}</h2>
        <p>{product.description}</p>
        <p className="product-card-price">{formatPrice(product.price)}</p>
        <p className="product-card-stock">{product.stock > 0 ? `${product.stock} en existencia` : 'Agotado'}</p>
        <div className="store-actions">
          <Link className="store-button store-button--secondary" to={`/productos/${product.id}/editar`} aria-label={`Editar ${product.name}`}>Editar</Link>
          <button className="store-button store-button--danger" type="button" disabled={disabled}
            aria-label={`Eliminar ${product.name}`} onClick={() => onDelete(product)}>
            {deleting ? 'Eliminando…' : 'Eliminar'}
          </button>
        </div>
      </div>
    </article>
  )
}
