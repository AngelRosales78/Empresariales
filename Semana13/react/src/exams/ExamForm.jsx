import { useState } from 'react'
import { createExam, describeError } from '../api/exams'

export default function ExamForm({ onCreated }) {
  const [title, setTitle] = useState('')
  const [saving, setSaving] = useState(false)
  const [fieldError, setFieldError] = useState('')
  const [error, setError] = useState('')

  async function submit(event) {
    event.preventDefault()
    setFieldError('')
    setError('')
    setSaving(true)
    try {
      const exam = await createExam({ title })
      onCreated(exam.title)
    } catch (failure) {
      const messages = failure.response?.data?.title
      if (Array.isArray(messages)) setFieldError(messages.join(' '))
      else setError(describeError(failure))
    } finally {
      setSaving(false)
    }
  }

  return (
    <>
      <header className="exam-heading"><div><h1>Nuevo examen</h1><p>Ingresa el título para registrar el examen.</p></div></header>
      <form className="exam-panel exam-form" noValidate onSubmit={submit}>
        <label htmlFor="exam-title">Título <span>(obligatorio)</span></label>
        <input id="exam-title" required value={title} onChange={(event) => { setTitle(event.target.value); setFieldError('') }}
          disabled={saving} aria-invalid={Boolean(fieldError)} aria-describedby={fieldError ? 'title-error' : undefined} />
        {fieldError && <p id="title-error" role="alert">{fieldError}</p>}
        {error && <p role="alert">{error}</p>}
        <div className="exam-form-actions">
          <button className="exam-button" type="submit" disabled={saving}>{saving ? 'Guardando…' : 'Guardar examen'}</button>
          <a href="#examenes">Cancelar</a>
        </div>
      </form>
    </>
  )
}
