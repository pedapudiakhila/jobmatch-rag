function MatchScore({ score }) {
  const normalizedScore = Math.min(
    Math.max(Number(score) || 0),
    100,
  )

  return (
    <div className="rounded-2xl border border-slate-200 bg-white p-8 text-center shadow-sm">
      <p className="text-sm font-semibold uppercase tracking-widest text-slate-500">
        Skill Match Score
      </p>

      <div className="mt-4">
        <span className="text-6xl font-bold tracking-tight text-slate-900">
          {normalizedScore}%
        </span>
      </div>

      <div className="mx-auto mt-6 h-3 max-w-md overflow-hidden rounded-full bg-slate-100">
        <div
          className="h-full rounded-full bg-blue-700 transition-all duration-700"
          style={{
            width: `${normalizedScore}%`,
          }}
        />
      </div>

      <p className="mx-auto mt-4 max-w-lg text-sm leading-6 text-slate-500">
        Based on the skills and requirements identified from
        the provided documents.
      </p>
    </div>
  )
}

export default MatchScore