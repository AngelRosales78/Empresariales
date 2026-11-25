export default function CategoryFilter({ categories, value, onChange }) {
  return (
    <div className="store-filter">
      <label htmlFor="category-filter">Categoría</label>
      <select id="category-filter" value={value} onChange={(event) => onChange(event.target.value)}>
        <option value="">Todas</option>
        {categories.map((category) => (
          <option key={category.id} value={category.id}>{category.name}</option>
        ))}
      </select>
    </div>
  )
}
