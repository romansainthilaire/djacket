import { defineStore } from "pinia"
import { ref } from "vue"
import api from "@/plugins/axios"

type User = {
  id: number
  email: string
  username: string
  isActive: boolean
  isStaff: boolean
  isSuperuser: boolean
  lastLogin: string
  createdAt: string
  updatedAt: string
}

type VerifyEmailResponse = {
  email?: string
  verified?: boolean
}

export type EditableUser = Pick<User, "username">

export const useAuthStore = defineStore("auth", () => {

  const token = ref<string | null>(localStorage.getItem("token"))
  const user = ref<User | null>(null)

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

  async function setUser() {
    if (!token.value) {
      return
    }
    try {
      const response = await api.get("users/me/")
      user.value = response.data
    } catch (error) {
      logout()
    }
  }

  async function login(email: string, password: string) {
    const response = await api.post("token/", { email, password })
    token.value = response.data.access
    localStorage.setItem("token", token.value!)
    await setUser()
  }

  function logout() {
    token.value = null
    user.value = null
    localStorage.removeItem("token")
  }

  async function editUser(data: Partial<EditableUser>) {
    if (!user.value) {
      return
    }
    const response = await api.patch(`users/${user.value.id}/`, data)
    user.value = response.data
  }

  return {
    token,
    user,
    signup,
    verifyEmail,
    resendVerificationEmail,
    setUser,
    editUser,
    login,
    logout
  }
})