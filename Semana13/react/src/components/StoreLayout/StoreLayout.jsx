import { Link, Outlet } from 'react-router-dom'
import './StoreLayout.css'

export default function StoreLayout() {
  return (
    <div className="store">
      <nav className="store-nav" aria-label="Navegación principal">
        <Link className="store-brand" to="/">Tienda Cinéclub</Link>
        <Link to="/examenes">Exámenes</Link>
        <Link to="/cartelera">Cartelera</Link>
      </nav>
      <main className="store-main"><Outlet /></main>
    </div>
  )
}
