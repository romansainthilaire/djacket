<script setup lang="ts">
import { ref, computed, watch } from "vue"
import { useRouter } from "vue-router"
import { useAuthStore } from "@/stores/auth"

import BaseForm from "@/components/BaseForm.vue"
import BaseFormField from "@/components/BaseFormField.vue"
import BaseLoadingSpinner from "@/components/BaseLoadingSpinner.vue"
import BaseButton from "@/components/BaseButton.vue"

const router = useRouter()
const auth = useAuthStore()

const oldPassword = ref("")
const newPassword = ref("")

const loading = ref(false)

const oldPasswordErrorMessage = ref("")
const newPasswordErrorMessage = ref("")
const unknownErrorMessage = ref("")

const passwordValidationRules = computed((): Array<{ text: string, checked: boolean }> => [
  { text: "Au moins 8 caractères", checked: newPassword.value.length >= 8 },
  { text: "Une lettre majuscule", checked: /[A-Z]/.test(newPassword.value) },
  { text: "Une lettre minuscule", checked: /[a-z]/.test(newPassword.value) },
  { text: "Un chiffre", checked: /\d/.test(newPassword.value) },
  { text: "Un caractère spécial (!@#$%^&* etc.)", checked: /[!@#$%^&*(),.?":{}|<>]/.test(newPassword.value) }
])

const newPasswordIsValid = computed(() =>
  passwordValidationRules.value.every(rule => rule.checked)
)

async function changePassword() {
  unknownErrorMessage.value = ""
  if (!newPasswordIsValid.value) {
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

    <BaseFormField
      id="old-password"
      label="Mot de passe actuel"
      v-model="oldPassword"
      type="password"
      required
      :error-message="oldPasswordErrorMessage"
    />

    <BaseFormField
      id="new-password"
      label="Nouveau mot de passe"
      v-model="newPassword"
      type="password"
      required
      :error-message="newPasswordErrorMessage"
    />

    <div class="password-validation-rules">
      Doit inclure :
      <ul>
        <li v-for="rule in passwordValidationRules" :key="rule.text" :class="{ 'checked': rule.checked }">
          <span>{{ rule.text }}</span>
        </li>
      </ul>
    </div>

    <p v-if="unknownErrorMessage" class="error-message">{{ unknownErrorMessage }}</p>

    <div class="submit-button-container">
      <BaseLoadingSpinner v-if="loading" />
      <BaseButton v-else type="submit">Changer mon mot de passe</BaseButton>
    </div>

  </BaseForm>
</template>

<style scoped>
.error-message {
  margin-top: 15px;
  font-size: 13px;
  color: var(--color-error);
}

.password-validation-rules {
  margin-top: 10px;
  font-size: 13px;
  color: rgb(100, 100, 100);
}

.password-validation-rules ul {
  list-style: none;
  margin-top: 5px;
}

.password-validation-rules li {
  position: relative;
  padding-left: 20px;
}

.password-validation-rules li::before {
  content: "•";
  position: absolute;
  left: 0;
  width: 15px;
  text-align: center;
}

.password-validation-rules li.checked::before {
  content: "✔";
  color: var(--color-success);
}

.submit-button-container {
  height: 100px;
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>