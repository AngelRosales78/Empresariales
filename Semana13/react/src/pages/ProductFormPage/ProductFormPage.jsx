import { useEffect, useState } from 'react'
import { Link, useNavigate, useParams } from 'react-router-dom'
import { describeError, getFieldErrors } from '../../services/apiClient'
import { listCategories } from '../../services/categoryService'
import { createProduct, getProduct, updateProduct } from '../../services/productService'
import './ProductFormPage.css'

const emptyForm = { name: '', description: '', price: '', stock: '0', category_id: '' }

function toForm(product) {
  return {
    name: product.name,
    description: product.description,
    price: product.price,
    stock: String(product.stock),
    category_id: String(product.category.id),
  }
}

function Field({ id, label, error, children }) {
  return (
    <div className="product-field">
      <label htmlFor={id}>{label}</label>
      {children}
      {error && <p className="store-error" id={`${id}-error`} role="alert">{error}</p>}
    </div>
  )
}

export default function ProductFormPage() {
  const { productId } = useParams()
  const navigate = useNavigate()
  const [form, setForm] = useState(emptyForm)
  const [image, setImage] = useState(null)
  const [currentImage, setCurrentImage] = useState('')
  const [categories, setCategories] = useState([])
  const [status, setStatus] = useState('loading')
  const [error, setError] = useState('')
  const [fieldErrors, setFieldErrors] = useState({})
  const [saving, setSaving] = useState(false)

  useEffect(() => {
    const controller = new AbortController()
    Promise.all([
      listCategories(controller.signal),
      productId ? getProduct(productId, controller.signal) : null,
    ])
      .then(([categoryList, product]) => {
        if (controller.signal.aborted) return
        setCategories(categoryList)
        if (product) {
          setForm(toForm(product))
          setCurrentImage(product.image ?? '')
        }
        setStatus('ready')
      })
      .catch((failure) => {
        if (controller.signal.aborted) return
        setError(describeError(failure))
        setStatus('error')
      })
    return () => controller.abort()
  }, [productId])

  function handleChange({ target }) {
    setForm((current) => ({ ...current, [target.name]: target.value }))
    setFieldErrors((current) => ({ ...current, [target.name]: '' }))
  }

  function fieldProps(name) {
    return {
      id: name,
      name,
      value: form[name],
      onChange: handleChange,
      disabled: saving,
      'aria-invalid': Boolean(fieldErrors[name]),
      'aria-describedby': fieldErrors[name] ? `${name}-error` : undefined,
    }
  }

  async function handleSubmit(event) {
    event.preventDefault()
    setSaving(true)
    setError('')
    setFieldErrors({})
    const payload = { ...form, image }
    try {
      const product = productId
        ? await updateProduct(productId, payload)
        : await createProduct(payload)
      const action = productId ? 'Se actualizó' : 'Se creó'
      navigate('/', { state: { notice: `${action} «${product.name}».` } })
    } catch (failure) {
      const errors = getFieldErrors(failure)
      if (Object.keys(errors).length) setFieldErrors(errors)
      else setError(describeError(failure))
      setSaving(false)
    }
  }

  return (
    <>
      <header className="store-heading"><h1>{productId ? 'Editar producto' : 'Nuevo producto'}</h1></header>
      {status === 'loading' && <p role="status">Cargando formulario…</p>}
      {error && <p className="store-error" role="alert">{error}</p>}
      {status === 'error' && <Link to="/">Volver al catálogo</Link>}
      {status === 'ready' && (
        <form className="product-form" onSubmit={handleSubmit}>
          <Field id="name" label="Nombre" error={fieldErrors.name}>
            <input {...fieldProps('name')} required maxLength={120} />
          </Field>
          <Field id="category_id" label="Categoría" error={fieldErrors.category_id}>
            <select {...fieldProps('category_id')} required>
              <option value="">Elige una categoría</option>
              {categories.map((category) => <option key={category.id} value={category.id}>{category.name}</option>)}
            </select>
          </Field>
          <Field id="description" label="Descripción" error={fieldErrors.description}>
            <textarea {...fieldProps('description')} rows={4} />
          </Field>
          <div className="product-form-row">
            <Field id="price" label="Precio (S/)" error={fieldErrors.price}>
              <input {...fieldProps('price')} type="number" min="0.01" step="0.01" required />
            </Field>
            <Field id="stock" label="Existencias" error={fieldErrors.stock}>
              <input {...fieldProps('stock')} type="number" min="0" step="1" required />
            </Field>
          </div>
          <Field id="image" label={currentImage ? 'Cambiar imagen (opcional)' : 'Imagen (opcional)'} error={fieldErrors.image}>
            {currentImage && <img src={currentImage} alt="Imagen actual del producto" />}
            <input id="image" type="file" accept="image/*" disabled={saving}
              onChange={(event) => setImage(event.target.files[0] ?? null)} />
          </Field>
          <div className="store-actions">
            <button className="store-button" type="submit" disabled={saving}>{saving ? 'Guardando…' : 'Guardar producto'}</button>
            <Link className="store-button store-button--secondary" to="/">Cancelar</Link>
          </div>
        </form>
      )}
    </>
  )
}
