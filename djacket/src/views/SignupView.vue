<script setup lang="ts">
import { ref, computed, watch } from "vue"
import { useRouter } from "vue-router"
import { useAuthStore } from "@/stores/auth"

import BaseForm from "@/components/BaseForm.vue"
import BaseFormField from "@/components/BaseFormField.vue"
import PasswordFieldWithValidation from "@/components/PasswordFieldWithValidation.vue"
import BaseLoadingSpinner from "@/components/BaseLoadingSpinner.vue"
import BaseButton from "@/components/BaseButton.vue"

const router = useRouter()
const auth = useAuthStore()

const email = ref("")
const username = ref("")
const password = ref("")
const passwordField = ref()

const loading = ref(false)

const emailErrorMessage = ref("")
const usernameErrorMessage = ref("")
const passwordErrorMessage = ref("")
const unknownErrorMessage = ref("")

const usernameIsValid = computed((): boolean =>
  username.value.length >= 3 && username.value.length <= 30
)

function validateForm(): boolean {
  let isValid = true
  if (!usernameIsValid.value) {
    usernameErrorMessage.value = "Le nom d'utilisateur doit contenir entre 3 et 30 caractères."
    isValid = false
  }
  if (!passwordField.value.passwordIsValid) {
    passwordErrorMessage.value = "Le mot de passe ne respecte pas les règles de sécurité."
    isValid = false
  }
  return isValid
}

async function signup() {
  unknownErrorMessage.value = ""
  if (!validateForm()) {
    return
  }
  loading.value = true
  try {
    await auth.signup(email.value, username.value, password.value)
    router.push({ name: "verify-email-notice", params: { email: email.value } })
  } catch (error: any) {
    if (error.response?.data) {
      const data = error.response.data
      emailErrorMessage.value = data.email ? data.email.join(" ") : ""
      usernameErrorMessage.value = data.username ? data.username.join(" ") : ""
      passwordErrorMessage.value = data.password ? data.password.join(" ") : ""
    } else {
      unknownErrorMessage.value = "Une erreur est survenue. Veuillez réessayer plus tard."
    }
  } finally {
    loading.value = false
  }
}

watch(email, () => {
  emailErrorMessage.value = ""
  unknownErrorMessage.value = ""
})

watch(username, () => {
  usernameErrorMessage.value = ""
  unknownErrorMessage.value = ""
})

watch(password, () => {
  passwordErrorMessage.value = ""
  unknownErrorMessage.value = ""
})
</script>

<template>
  <BaseForm title="Inscription" @submit="signup()">

    <BaseFormField
      v-model="email"
      id="email"
      type="email"
      label="Adresse e-mail"
      required
      :error-message="emailErrorMessage"
    />

    <BaseFormField
      v-model="username"
      id="username"
      type="text"
      label="Nom d'utilisateur"
      required
      :error-message="usernameErrorMessage"
    />

    <PasswordFieldWithValidation
      v-model="password"
      ref="passwordField"
      id="password"
      label="Mot de passe"
      required
      :error-message="passwordErrorMessage"
    />

    <p v-if="unknownErrorMessage" class="error-message">{{ unknownErrorMessage }}</p>
    
    <div class="submit-button-container">
      <BaseLoadingSpinner v-if="loading" />
      <BaseButton v-else type="submit">Créer mon compte</BaseButton>
    </div>

    <div class="footer">
      <div class="footer-text">Vous possédez déjà un compte ?</div>
      <RouterLink class="footer-link" to="/login">Me connecter</RouterLink>
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

.footer {
  text-align: center;
  padding-bottom: 30px;
}

.footer-text {
  font-size: 13px;
  color: rgb(100, 100, 100);
  margin-bottom: 5px;
}

.footer-link {
  font-size: 14px;
  color: rgb(20, 150, 250);
  text-underline-offset: 2px;
}
</style>
