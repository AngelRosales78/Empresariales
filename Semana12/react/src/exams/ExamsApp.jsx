import { useEffect, useState } from 'react'
import ExamForm from './ExamForm'
import ExamList from './ExamList'
import './exams.css'

export default function ExamsApp() {
  const [form, setForm] = useState(() => location.hash === '#nuevo')
  const [notice, setNotice] = useState('')

  useEffect(() => {
    function updateRoute() {
      const isForm = location.hash === '#nuevo'
      setForm(isForm)
      if (isForm) setNotice('')
    }
    window.addEventListener('hashchange', updateRoute)
    return () => window.removeEventListener('hashchange', updateRoute)
  }, [])

  function onCreated(title) {
    if (location.hash !== '#nuevo') return
    setNotice(`Se creó el examen «${title}».`)
    location.hash = '#examenes'
  }

  return (
    <div className="exam-app">
      <nav className="exam-nav" aria-label="Navegación principal">
        <a href="#examenes">Gestión de exámenes</a>
        <a href="/cartelera">Cartelera</a>
      </nav>
      <main className="exam-main">
        {notice && !form && <p className="exam-notice" role="status">{notice}</p>}
        {form ? <ExamForm onCreated={onCreated} /> : <ExamList />}
      </main>
    </div>
  )
}
