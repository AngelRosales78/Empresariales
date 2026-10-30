export default function Button({ children, variant = 'secondary', type = 'button', className = '', ...props }) {
  return (
    <button type={type} className={`button button--${variant} ${className}`.trim()} {...props}>
      {children}
    </button>
  )
}
