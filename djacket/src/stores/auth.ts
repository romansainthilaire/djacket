import { defineStore } from "pinia"
import { ref } from "vue"
import api from "@/plugins/axios"
import { useUserStore } from "@/stores/user"


type VerifyEmailResponse = {
  email?: string
  verified?: boolean
}

export const useAuthStore = defineStore("auth", () => {

  const token = ref<string | null>(localStorage.getItem("token"))
  const userStore = useUserStore()

  async function signup(email: string, username: string, password: string) {
    await api.post("users/", { email, username, password })
  }

  async function verifyEmail(token: string): Promise<VerifyEmailResponse> {
    try {
      const response = await api.get(`users/verify-email/?token=${token}`)
      return { email: response.data.email, verified: true }
    } catch (error: any) {
      const status = error.response?.status
      const data = error.response?.data
      if (status == 410) {
        return { email: data.email, verified: false }
      }
      return { verified: false }
    }
  }

  async function resendVerificationEmail(email: string) {
    await api.post("users/resend-verification-email/", { email })
  }

  async function resetPassword(email: string) {
    await api.post("users/reset-password/", { email })
  }

  async function login(email: string, password: string) {
    const response = await api.post("token/", { email, password })
    token.value = response.data.access
    localStorage.setItem("token", token.value!)
    await userStore.fetchUser()
  }

  function logout() {
    token.value = null
    localStorage.removeItem("token")
    userStore.clearUser()
  }

  return {
    token,
    signup,
    verifyEmail,
    resendVerificationEmail,
    resetPassword,
    login,
    logout
  }
})
