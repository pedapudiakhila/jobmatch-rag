import { useState } from "react"

import Navbar from "../components/Navbar"
import FileUpload from "../components/FileUpload"
import MatchScore from "../components/MatchScore"
import ListSection from "../components/ListSection"
import { analyzeJobMatch } from "../services/api"
import QuestionAnswer from "../components/QuestionAnswer"

function Home() {
  const [resume, setResume] = useState(null)
  const [jobDescription, setJobDescription] = useState(null)

  const [result, setResult] = useState(null)

  const [loading, setLoading] = useState(false)
  const [error, setError] = useState("")


  const handleAnalyze = async () => {
    if (!resume || !jobDescription) {
      setError(
        "Please upload both your resume and the job description.",
      )

      return
    }

    setError("")
    setResult(null)
    setLoading(true)

    try {
      const response = await analyzeJobMatch(
        resume,
        jobDescription,
      )

      if (!response?.success) {
        throw new Error(
          response?.message ||
            "Unable to analyze the documents.",
        )
      }

      setResult(response.data)

} catch (err) {
  console.error(
    "Job match analysis failed:",
    err,
  )

  if (err.response?.status === 429) {
    setError(
      "Gemini API quota is temporarily exhausted. Please try again later.",
    )
  } else {
    setError(
      err.response?.data?.detail ||
        err.message ||
        "Something went wrong while analyzing the documents.",
    )
  }

} finally {
  setLoading(false)
}
  }


  return (
    <div className="min-h-screen bg-slate-50 text-slate-900">

      <Navbar />


      <main className="mx-auto max-w-6xl px-6 py-14 sm:py-20">

        {/* Hero */}

        <section className="relative text-center">

          <div className="pointer-events-none absolute left-1/2 top-0 -z-0 h-40 w-72 -translate-x-1/2 rounded-full bg-blue-100/60 blur-3xl" />

          <div className="relative z-10 mx-auto max-w-3xl">

            <div className="mx-auto inline-flex items-center rounded-full border border-blue-100 bg-blue-50 px-4 py-2 text-xs font-semibold uppercase tracking-widest text-blue-700">
              AI-Powered Resume Intelligence
            </div>

            <h1 className="mt-6 text-4xl font-bold tracking-tight text-slate-950 sm:text-5xl lg:text-6xl">
              Find your match
              <span className="block text-blue-700">
                for any job.
              </span>
            </h1>

            <p className="mx-auto mt-6 max-w-2xl text-base leading-7 text-slate-600 sm:text-lg">
              Compare your resume with a job description and
              discover matching skills, missing requirements,
              strengths, and potential gaps.
            </p>

          </div>

        </section>


        {/* Upload Section */}

        <section className="mt-14 grid gap-6 md:grid-cols-2">

          <FileUpload
  inputId="resume-file-input"
  title="Upload Resume"
  description="Upload your latest resume in PDF format."
  file={resume}
  onFileSelect={(file) => {
    setResume(file)
    setError("")
  }}
/>

<FileUpload
  inputId="job-description-file-input"
  title="Upload Job Description"
  description="Upload the job description you want to analyze."
  file={jobDescription}
  onFileSelect={(file) => {
    setJobDescription(file)
    setError("")
  }}
/>

        </section>


        {/* Error */}

        {error && (

          <div className="mx-auto mt-6 max-w-2xl rounded-xl border border-rose-200 bg-rose-50 px-5 py-4 text-center text-sm font-medium text-rose-700">
            {error}
          </div>

        )}


        {/* Analyze Button */}

        <div className="mt-8 flex justify-center">

          <button
            onClick={handleAnalyze}
            disabled={loading}
            className="rounded-xl bg-blue-700 px-8 py-3.5 text-sm font-semibold text-white shadow-lg shadow-blue-700/20 transition hover:bg-blue-800 active:scale-[0.98] disabled:cursor-not-allowed disabled:opacity-60"
          >
            {loading ? "Analyzing..." : "Analyze Job Match"}
          </button>

        </div>


        {/* Loading */}

        {loading && (

          <div className="mt-8 text-center">

            <div className="inline-flex items-center gap-3 rounded-xl border border-blue-100 bg-blue-50 px-5 py-3 text-sm font-medium text-blue-700">

              <div className="h-4 w-4 animate-spin rounded-full border-2 border-blue-200 border-t-blue-700" />

              Analyzing your resume against the job description...

            </div>

          </div>

        )}


{/* Results */}

{result && !loading && (

  <section className="mt-20">

    <div className="mb-8 text-center">

      <div className="mx-auto inline-flex items-center gap-2 rounded-full bg-emerald-50 px-4 py-2 text-xs font-semibold uppercase tracking-widest text-emerald-700">

        <span className="h-2 w-2 rounded-full bg-emerald-500" />

        Analysis Complete

      </div>

      <h2 className="mt-4 text-3xl font-bold tracking-tight text-slate-950">
        Your Job Match
      </h2>

      <p className="mt-2 text-sm text-slate-500">
        Here's how your profile compares with the role.
      </p>

    </div>


            <MatchScore
              score={result.match_score}
            />


            <div className="mt-6 grid gap-6 md:grid-cols-2">

              <ListSection
                title="Matching Skills"
                items={result.matching_skills}
                type="matching"
              />

              <ListSection
                title="Missing Skills"
                items={result.missing_skills}
                type="missing"
              />

              <ListSection
                title="Strengths"
                items={result.strengths}
                type="strength"
              />

              <ListSection
                title="Potential Gaps"
                items={result.gaps}
                type="gap"
              />

            </div>
<QuestionAnswer />

            {/* Relevant Experience */}

            {result.relevant_experience?.length > 0 && (

              <div className="mt-6">

                <ListSection
                  title="Relevant Experience"
                  items={result.relevant_experience}
                  type="strength"
                />

              </div>

            )}

          </section>

        )}

      </main>


      {/* Footer */}

      <footer className="border-t border-slate-200 bg-white py-8">

        <p className="text-center text-sm text-slate-500">
          JobMatch RAG · AI-Powered Resume Intelligence
        </p>

      </footer>

    </div>
  )
}

export default Home