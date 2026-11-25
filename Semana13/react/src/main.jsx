import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './styles/index.css'
import App from './App.jsx'
import ExamsApp from './exams/ExamsApp.jsx'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    {location.pathname === '/cartelera' ? <App /> : <ExamsApp />}
  </StrictMode>,
)
