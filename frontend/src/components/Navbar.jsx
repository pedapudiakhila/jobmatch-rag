function Navbar() {
  return (
    <nav className="border-b border-slate-200 bg-white">
      <div className="mx-auto flex max-w-6xl items-center justify-between px-6 py-5">
        <div>
          <h1 className="text-xl font-bold tracking-tight text-slate-900">
            JobMatch <span className="text-blue-700">RAG</span>
          </h1>

          <p className="mt-0.5 text-xs text-slate-500">
            Intelligent Resume Matching
          </p>
        </div>

        <div className="hidden rounded-full border border-slate-200 bg-slate-50 px-4 py-2 text-sm font-medium text-slate-600 sm:block">
          AI-Powered Career Analysis
        </div>
      </div>
    </nav>
  )
}

export default Navbar