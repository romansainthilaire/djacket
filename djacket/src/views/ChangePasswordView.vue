<script setup lang="ts">
import { ref, useTemplateRef, watch } from "vue"
import { useRouter } from "vue-router"
import { useAuthStore } from "@/stores/auth"

import BaseForm from "@/components/BaseForm.vue"
import BaseInputPassword from "@/components/BaseInputPassword.vue"
import BaseInputPasswordWithValidation from "@/components/BaseInputPasswordWithValidation.vue"
import BaseLoadingSpinner from "@/components/BaseLoadingSpinner.vue"
import BaseButton from "@/components/BaseButton.vue"

const router = useRouter()
const auth = useAuthStore()

const oldPassword = ref("")
const newPassword = ref("")
const newPasswordRef = useTemplateRef("newPasswordRef")
const loading = ref(false)

const oldPasswordErrorMessage = ref("")
const newPasswordErrorMessage = ref("")
const unknownErrorMessage = ref("")

async function changePassword() {
  unknownErrorMessage.value = ""
  if (!newPasswordRef.value?.passwordIsValid) {
    newPasswordErrorMessage.value = "Le nouveau mot de passe ne respecte pas les règles de sécurité."
    return
  } else if (oldPassword.value == newPassword.value) {
    newPasswordErrorMessage.value = "Le nouveau mot de passe doit être différent de l'ancien."
    return
  }
  loading.value = true
  try {
    await auth.changePassword(oldPassword.value, newPassword.value)
    router.push({ path: "/user-account", query: { modified: "true" } })
  } catch (error: any) {
    if (error.response?.data) {
      const data = error.response.data
      oldPasswordErrorMessage.value = data.old_password ? "Mot de passe incorrect." : ""
      newPasswordErrorMessage.value = data.new_password ? data.new_password.join(" ") : ""
    } else {
      unknownErrorMessage.value = "Une erreur est survenue. Veuillez réessayer plus tard."
    }
  } finally {
    loading.value = false
  }
}

watch(oldPassword, () => {
  oldPasswordErrorMessage.value = ""
  unknownErrorMessage.value = ""
})

watch(newPassword, () => {
  newPasswordErrorMessage.value = ""
  unknownErrorMessage.value = ""
})
</script>

<template>
  <BaseForm title="Modification du mot de passe" @submit="changePassword()">

    <BaseInputPassword
      v-model="oldPassword"
      id="old-password"
      label="Mot de passe actuel"
      required
      :error-message="oldPasswordErrorMessage"
    />

    <BaseInputPasswordWithValidation
      v-model="newPassword"
      ref="newPasswordRef"
      id="new-password"
      label="Nouveau mot de passe"
      required
      :error-message="newPasswordErrorMessage"
    />

    <p v-if="unknownErrorMessage" class="error-message">{{ unknownErrorMessage }}</p>

    <div class="submit-button-container">
      <BaseLoadingSpinner v-if="loading" />
      <BaseButton v-else type="submit">Enregistrer</BaseButton>
    </div>

  </BaseForm>
</template>

<style scoped>
.error-message {
  margin-top: 15px;
  font-size: 13px;
  color: var(--color-error);
}

.submit-button-container {
  height: 100px;
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>
