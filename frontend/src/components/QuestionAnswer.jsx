import { useState } from "react"
import { askQuestion } from "../services/api"
import ReactMarkdown from "react-markdown"

const suggestedQuestions = [
  "What technical skills does the candidate have?",
  "Does the candidate have AI experience?",
  "Does the candidate have AWS experience?",
  "What backend technologies has the candidate used?",
]


function QuestionAnswer() {
  const [question, setQuestion] = useState("")
  const [answer, setAnswer] = useState(null)

  const [loading, setLoading] = useState(false)
  const [error, setError] = useState("")


  const handleAsk = async (customQuestion = null) => {

    const currentQuestion = (
      customQuestion ?? question
    ).trim()

    if (!currentQuestion) {
      setError("Please enter a question.")
      return
    }

    setQuestion(currentQuestion)
    setError("")
    setAnswer(null)
    setLoading(true)

    try {

      const response = await askQuestion(
        currentQuestion,
      )

      if (!response?.success) {
        throw new Error(
          response?.message ||
            "Unable to answer the question.",
        )
      }

      setAnswer(response.data)

    } catch (err) {

      console.error(
        "Question answering failed:",
        err,
      )

      setError(
        err.response?.data?.detail ||
          err.message ||
          "Something went wrong while answering your question.",
      )

    } finally {

      setLoading(false)

    }
  }


  const handleSuggestedQuestion = (
    suggestedQuestion,
  ) => {
    handleAsk(suggestedQuestion)
  }


  return (
    <section className="mt-10 overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-sm">

      {/* Header */}

      <div className="border-b border-slate-200 bg-slate-950 px-6 py-6 sm:px-8">

        <div className="flex items-start gap-4">

          <div className="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl bg-white/10 text-white">

            <svg
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="1.8"
              className="h-5 w-5"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                d="M8.5 10.5h7M8.5 14h4M12 3.75a8.25 8.25 0 0 0-7.18 12.32L4 20.25l4.18-1.39A8.25 8.25 0 1 0 12 3.75Z"
              />
            </svg>

          </div>


          <div>

            <p className="text-xs font-semibold uppercase tracking-[0.18em] text-blue-300">
              RAG Assistant
            </p>

            <h3 className="mt-1 text-xl font-bold text-white">
              Ask about the candidate
            </h3>

            <p className="mt-2 max-w-2xl text-sm leading-6 text-slate-300">
              Ask questions about skills, projects,
              experience, education, or other information
              found in the uploaded resume.
            </p>

          </div>

        </div>

      </div>


      {/* Body */}

      <div className="p-6 sm:p-8">


        {/* Question input */}

        <div className="flex flex-col gap-3 sm:flex-row">

          <input
            type="text"
            value={question}
            onChange={(event) => {
              setQuestion(event.target.value)
              setError("")
            }}
            onKeyDown={(event) => {
              if (event.key === "Enter") {
                handleAsk()
              }
            }}
            placeholder="Ask a question about the candidate..."
            disabled={loading}
            className="min-w-0 flex-1 rounded-xl border border-slate-300 bg-white px-4 py-3.5 text-sm text-slate-900 outline-none transition placeholder:text-slate-400 focus:border-blue-700 focus:ring-4 focus:ring-blue-100 disabled:bg-slate-50"
          />


          <button
            onClick={() => handleAsk()}
            disabled={loading}
            className="rounded-xl bg-blue-700 px-7 py-3.5 text-sm font-semibold text-white transition hover:bg-blue-800 disabled:cursor-not-allowed disabled:opacity-60"
          >
            {loading ? "Searching..." : "Ask"}
          </button>

        </div>


        {/* Suggested questions */}

        {!answer && !loading && (

          <div className="mt-6">

            <p className="text-xs font-semibold uppercase tracking-widest text-slate-400">
              Try asking
            </p>

            <div className="mt-3 flex flex-wrap gap-2">

              {suggestedQuestions.map(
                (suggestedQuestion) => (

                  <button
                    key={suggestedQuestion}
                    onClick={() =>
                      handleSuggestedQuestion(
                        suggestedQuestion,
                      )
                    }
                    className="rounded-full border border-slate-200 bg-slate-50 px-4 py-2 text-left text-xs font-medium text-slate-600 transition hover:border-blue-200 hover:bg-blue-50 hover:text-blue-700"
                  >
                    {suggestedQuestion}
                  </button>

                ),
              )}

            </div>

          </div>

        )}


        {/* Error */}

        {error && (

          <div className="mt-5 rounded-xl border border-rose-200 bg-rose-50 px-4 py-3 text-sm leading-6 text-rose-700">
            {error}
          </div>

        )}


        {/* Loading */}

        {loading && (

          <div className="mt-6 rounded-xl border border-blue-100 bg-blue-50 px-5 py-5">

            <div className="flex items-center gap-3">

              <div className="h-5 w-5 animate-spin rounded-full border-2 border-blue-200 border-t-blue-700" />

              <div>

                <p className="text-sm font-semibold text-blue-800">
                  Searching the resume...
                </p>

                <p className="mt-1 text-xs text-blue-600">
                  Retrieving relevant context and generating
                  a grounded answer.
                </p>

              </div>

            </div>

          </div>

        )}


        {/* Answer */}

        {answer && !loading && (

          <div className="mt-7 space-y-5">

            {/* Answer card */}

            <div className="rounded-xl border border-slate-200 bg-slate-50 p-5">

              <div className="flex items-center justify-between">

                <p className="text-xs font-semibold uppercase tracking-widest text-slate-500">
                  Answer
                </p>

                <span className="rounded-full bg-emerald-50 px-3 py-1 text-[11px] font-semibold text-emerald-700">
                  RAG Grounded
                </span>

              </div>


              <div className="prose prose-sm max-w-none text-slate-700">
  <ReactMarkdown>
    {answer.answer}
  </ReactMarkdown>
</div>

            </div>


            {/* Sources */}

            {answer.sources?.length > 0 && (

              <div>

                <div className="flex items-center gap-2">

                  <p className="text-xs font-semibold uppercase tracking-widest text-slate-500">
                    Sources
                  </p>

                  <span className="rounded-full bg-slate-100 px-2 py-0.5 text-[10px] font-semibold text-slate-500">
                    {answer.sources.length}
                  </span>

                </div>


                <div className="mt-3 grid gap-2 sm:grid-cols-2">

                  {answer.sources.map(
                    (source, index) => (

                      <div
                        key={`${source.source}-${source.page}-${index}`}
                        className="flex items-center gap-3 rounded-xl border border-slate-200 bg-white px-4 py-3"
                      >

                        <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg bg-blue-50 text-blue-700">

                          <svg
                            xmlns="http://www.w3.org/2000/svg"
                            viewBox="0 0 24 24"
                            fill="none"
                            stroke="currentColor"
                            strokeWidth="1.8"
                            className="h-4 w-4"
                          >
                            <path
                              strokeLinecap="round"
                              strokeLinejoin="round"
                              d="M6.75 3.75h7.5L18 7.5v12.75H6.75V3.75Z"
                            />

                            <path
                              strokeLinecap="round"
                              strokeLinejoin="round"
                              d="M14.25 3.75V7.5H18"
                            />
                          </svg>

                        </div>


                        <div className="min-w-0">

                          <p className="truncate text-sm font-medium text-slate-700">
                            {source.source}
                          </p>

                          <p className="mt-0.5 text-xs text-slate-400">
                            Page {source.page}
                          </p>

                        </div>

                      </div>

                    ),
                  )}

                </div>

              </div>

            )}


            {/* Ask another */}

            <button
              onClick={() => {
                setQuestion("")
                setAnswer(null)
                setError("")
              }}
              className="text-sm font-semibold text-blue-700 transition hover:text-blue-900"
            >
              ← Ask another question
            </button>

          </div>

        )}

      </div>

    </section>
  )
}

export default QuestionAnswer