import { useEffect, useState } from 'react'
import { Link, useLocation, useSearchParams } from 'react-router-dom'
import CategoryFilter from '../../components/CategoryFilter/CategoryFilter'
import ProductCard from '../../components/ProductCard/ProductCard'
import { describeError } from '../../services/apiClient'
import { listCategories } from '../../services/categoryService'
import { deleteProduct, listProducts } from '../../services/productService'
import './CatalogPage.css'

export default function CatalogPage() {
  const location = useLocation()
  const [searchParams, setSearchParams] = useSearchParams()
  const category = searchParams.get('categoria') ?? ''
  const [categories, setCategories] = useState([])
  const [categoriesError, setCategoriesError] = useState('')
  const [result, setResult] = useState({ key: null, products: [], error: '' })
  const [deleteError, setDeleteError] = useState('')
  const [deletingId, setDeletingId] = useState(null)
  const [notice, setNotice] = useState(location.state?.notice ?? '')
  const [attempt, setAttempt] = useState(0)

  // A result that belongs to another request means this one is still loading.
  const requestKey = `${category}|${attempt}`
  const { products, error } = result
  const loading = result.key !== requestKey

  useEffect(() => {
    const controller = new AbortController()
    listCategories(controller.signal)
      .then((data) => {
        if (controller.signal.aborted) return
        setCategories(data)
        setCategoriesError('')
      })
      .catch((failure) => {
        if (!controller.signal.aborted) setCategoriesError(describeError(failure))
      })
    return () => controller.abort()
  }, [attempt])

  useEffect(() => {
    const controller = new AbortController()
    listProducts({ category, signal: controller.signal })
      .then((data) => {
        if (!controller.signal.aborted) setResult({ key: requestKey, products: data, error: '' })
      })
      .catch((failure) => {
        if (!controller.signal.aborted) setResult({ key: requestKey, products: [], error: describeError(failure) })
      })
    return () => controller.abort()
  }, [category, requestKey])

  function changeCategory(value) {
    setNotice('')
    setDeleteError('')
    setSearchParams(value ? { categoria: value } : {})
  }

  async function handleDelete(product) {
    if (!window.confirm(`¿Eliminar «${product.name}»?`)) return
    setNotice('')
    setDeleteError('')
    setDeletingId(product.id)
    try {
      await deleteProduct(product.id)
      setResult((current) => ({
        ...current,
        products: current.products.filter((item) => item.id !== product.id),
      }))
      setNotice(`Se eliminó «${product.name}».`)
    } catch (failure) {
      setDeleteError(describeError(failure))
    } finally {
      setDeletingId(null)
    }
  }

  function renderProducts() {
    if (loading) return <p role="status">Cargando productos…</p>
    if (error) {
      return (
        <div>
          <p className="store-error" role="alert">{error}</p>
          <button className="store-button" type="button" onClick={() => setAttempt(attempt + 1)}>Reintentar</button>
        </div>
      )
    }
    if (!products.length) return <p>No hay productos para mostrar.</p>
    return (
      <section className="catalog-grid" aria-label="Productos">
        {products.map((product) => (
          <ProductCard key={product.id} product={product} onDelete={handleDelete}
            deleting={deletingId === product.id} disabled={deletingId !== null} />
        ))}
      </section>
    )
  }

  return (
    <>
      <header className="store-heading">
        <h1>Catálogo</h1>
        <Link className="store-button" to="/productos/nuevo">Nuevo producto</Link>
      </header>
      <CategoryFilter categories={categories} value={category} onChange={changeCategory} />
      {categoriesError && !error && <p className="store-error" role="alert">No se cargaron las categorías. {categoriesError}</p>}
      {notice && <p className="store-notice" role="status">{notice}</p>}
      {deleteError && <p className="store-error" role="alert">{deleteError}</p>}
      {renderProducts()}
    </>
  )
}
