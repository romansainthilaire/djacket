import axios from "axios"

import type {
    AxiosInstance,
    InternalAxiosRequestConfig,
    AxiosResponse
} from "axios"

import camelcaseKeys from "camelcase-keys"
import snakecaseKeys from "snakecase-keys"


const api: AxiosInstance = axios.create({
  baseURL: "http://127.0.0.1:8000/api/v1/",
  headers: {
    "Content-Type": "application/json"
  }
})

api.interceptors.request.use((config: InternalAxiosRequestConfig) => {
  const token = localStorage.getItem("token")
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  if (config.data) {
    config.data = snakecaseKeys(config.data, { deep: true })
  }
  if (config.params) {
    config.params = snakecaseKeys(config.params, { deep: true })
  }
  return config
})

api.interceptors.response.use((response: AxiosResponse) => {
  if (response.data) {
      response.data = camelcaseKeys(response.data, { deep: true })
  }
  return response
})

export default api
