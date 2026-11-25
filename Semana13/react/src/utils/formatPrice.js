const priceFormat = new Intl.NumberFormat('es-PE', { style: 'currency', currency: 'PEN' })

export default function formatPrice(price) {
  return priceFormat.format(Number(price))
}
