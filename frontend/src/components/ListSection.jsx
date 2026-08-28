function ListSection({
  title,
  items = [],
  type = "default",
}) {
  const getIcon = () => {
    if (type === "matching") {
      return "✓"
    }

    if (type === "missing") {
      return "✕"
    }

    if (type === "strength") {
      return "★"
    }

    if (type === "gap") {
      return "!"
    }

    return "•"
  }

  const getIconStyle = () => {
    if (type === "matching") {
      return "bg-emerald-50 text-emerald-600"
    }

    if (type === "missing") {
      return "bg-rose-50 text-rose-600"
    }

    if (type === "strength") {
      return "bg-blue-50 text-blue-700"
    }

    if (type === "gap") {
      return "bg-amber-50 text-amber-600"
    }

    return "bg-slate-100 text-slate-600"
  }

  return (
    <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
      <h3 className="text-lg font-semibold text-slate-900">
        {title}
      </h3>

      {items.length === 0 ? (
        <p className="mt-4 text-sm text-slate-500">
          No information available.
        </p>
      ) : (
        <ul className="mt-5 space-y-3">
          {items.map((item, index) => (
            <li
              key={`${item}-${index}`}
              className="flex items-start gap-3 rounded-xl bg-slate-50 px-3 py-3 text-sm leading-6 text-slate-700"
            >
              <span
                className={`mt-0.5 flex h-6 w-6 shrink-0 items-center justify-center rounded-full text-xs font-bold ${getIconStyle()}`}
              >
                {getIcon()}
              </span>

              <span>{item}</span>
            </li>
          ))}
        </ul>
      )}
    </div>
  )
}

export default ListSection