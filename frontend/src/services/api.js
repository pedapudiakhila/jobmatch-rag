import axios from "axios"


const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL ||
  "http://127.0.0.1:8000"


const api = axios.create({
  baseURL: API_BASE_URL,
})


export const analyzeJobMatch = async (
  resume,
  jobDescription,
) => {

  const formData = new FormData()

  formData.append(
    "resume",
    resume,
  )

  formData.append(
    "job_description",
    jobDescription,
  )

  const response = await api.post(
    "/api/analyze",
    formData,
  )

  return response.data
}


export const askQuestion = async (
  question,
) => {

  const response = await api.post(
    "/api/ask",
    {
      question,
    },
  )

  return response.data
}


export default api