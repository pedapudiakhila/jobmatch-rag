function FileUpload({
  title,
  description,
  file,
  onFileSelect,
}) {
  const handleChange = (event) => {
    const selectedFile = event.target.files?.[0]

    if (!selectedFile) {
      return
    }

    if (selectedFile.type !== "application/pdf") {
      alert("Please select a PDF file.")
      return
    }

    onFileSelect(selectedFile)
  }

  return (
    <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm transition hover:border-blue-200 hover:shadow-md">
      <div className="flex h-full flex-col">
        <div className="mb-5">
          <h2 className="text-lg font-semibold text-slate-900">
            {title}
          </h2>

          <p className="mt-1 text-sm text-slate-500">
            {description}
          </p>
        </div>

        <label className="group flex min-h-48 cursor-pointer flex-1 flex-col items-center justify-center rounded-xl border-2 border-dashed border-slate-300 bg-slate-50 px-6 text-center transition hover:border-blue-500 hover:bg-blue-50/40">
          <div className="mb-4 flex h-12 w-12 items-center justify-center rounded-xl bg-blue-50 text-2xl">
            📄
          </div>

          {file ? (
            <>
              <p className="max-w-full truncate font-semibold text-blue-700">
                {file.name}
              </p>

              <p className="mt-2 text-xs font-medium text-emerald-600">
                PDF selected successfully
              </p>
            </>
          ) : (
            <>
              <p className="font-medium text-slate-700">
                Choose a PDF file
              </p>

              <p className="mt-2 text-xs text-slate-500">
                Click to browse your files
              </p>
            </>
          )}

          <input
            type="file"
            accept=".pdf,application/pdf"
            className="hidden"
            onChange={handleChange}
          />
        </label>
      </div>
    </div>
  )
}

export default FileUpload