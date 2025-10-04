import axios, {AxiosError, type AxiosRequestConfig, type AxiosResponse} from "axios"
import {toast} from "sonner"

export const backend = axios.create({ baseURL: import.meta.env.VITE_BACKEND_BASE_URL })

export function getAbsoluteBackendURL(relativeURL: string) {
  return import.meta.env.VITE_BACKEND_BASE_URL + relativeURL
}

export async function sendBackendRequest<T = any, R = AxiosResponse<T>, D = any>(config: AxiosRequestConfig<D>): Promise<R> {
  try {
    return await backend.request<T, R, D>(config)
  } catch (_error) {
    if (!(_error instanceof AxiosError)) {
      throw _error
    }

    // output proper error message as a Toast notification
    const error: AxiosError = _error
    let title: string = "Error while communicating with the backend"
    let description: string = error.message
    if(error.response) {
      title = error.response.statusText
      let responseData: any = error.response.data
      if(Object.hasOwn(responseData, "detail")) {
        description = responseData.detail
      } else {
        description = error.message
      }
    }
    toast.error(title, {
      description: description
    })

    throw _error
  }
}