import { defineStore } from "pinia"
import { ref } from "vue"
import api from "@/plugins/axios"
import { useAuthStore } from "@/stores/auth"


type User = {
  id: number
  email: string
  username: string
  mustChangePassword: boolean
  isActive: boolean
  isStaff: boolean
  isSuperuser: boolean
  lastLogin: string
  createdAt: string
  updatedAt: string
}

type EditableUser = Pick<User, "username">

export const useUserStore = defineStore("user", () => {

  const user = ref<User | null>(null)
  const authStore = useAuthStore()

  async function fetchUser() {
    if (!authStore.token) {
      return
    }
    try {
      const response = await api.get("users/me/")
      user.value = response.data
    } catch {
      authStore.logout()
    }
  }

  function clearUser() {
    user.value = null
  }

  async function editUser(data: Partial<EditableUser>) {
    if (!user.value) {
      return
    }
    const response = await api.patch(`users/${user.value.id}/`, data)
    user.value = response.data
  }

  async function changePassword(oldPassword: string, newPassword: string) {
    if (!user.value) {
      return
    }
    await api.put("users/change-password/", { oldPassword, newPassword })
    user.value.mustChangePassword = false
  }

  return {
    user,
    fetchUser,
    clearUser,
    editUser,
    changePassword
  }
})
