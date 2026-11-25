import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom'
import './styles/index.css'
import App from './App.jsx'
import StoreLayout from './components/StoreLayout/StoreLayout.jsx'
import ExamsApp from './exams/ExamsApp.jsx'
import CatalogPage from './pages/CatalogPage/CatalogPage.jsx'
import ProductFormPage from './pages/ProductFormPage/ProductFormPage.jsx'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <BrowserRouter>
      <Routes>
        <Route element={<StoreLayout />}>
          <Route index element={<CatalogPage />} />
          <Route path="productos/nuevo" element={<ProductFormPage key="new" />} />
          <Route path="productos/:productId/editar" element={<ProductFormPage key="edit" />} />
        </Route>
        <Route path="examenes" element={<ExamsApp />} />
        <Route path="cartelera" element={<App />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  </StrictMode>,
)
