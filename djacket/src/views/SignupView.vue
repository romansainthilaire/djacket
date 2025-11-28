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

const email = ref("")
const username = ref("")
const password = ref("")

const loading = ref(false)

const emailErrorMessage = ref("")
const usernameErrorMessage = ref("")
const passwordErrorMessage = ref("")
const unknownErrorMessage = ref("")

const passwordValidationRules = computed((): Array<{ text: string, checked: boolean }> => [
  { text: "Au moins 8 caractères", checked: password.value.length >= 8 },
  { text: "Une lettre majuscule", checked: /[A-Z]/.test(password.value) },
  { text: "Une lettre minuscule", checked: /[a-z]/.test(password.value) },
  { text: "Un chiffre", checked: /\d/.test(password.value) },
  { text: "Un caractère spécial (!@#$%^&* etc.)", checked: /[!@#$%^&*(),.?":{}|<>]/.test(password.value) }
])

const usernameIsValid = computed((): boolean =>
  username.value.length >= 3 && username.value.length <= 30
)

const passwordIsValid = computed((): boolean =>
  passwordValidationRules.value.every(rule => rule.checked)
)

function validateForm(): boolean {
  let isValid = true
  if (!usernameIsValid.value) {
    usernameErrorMessage.value = "Le nom d'utilisateur doit contenir entre 3 et 30 caractères."
    isValid = false
  }
  if (!passwordIsValid.value) {
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
      id="email"
      label="Adresse e-mail"
      v-model="email"
      type="email"
      required
      :error-message="emailErrorMessage"
    />

    <BaseFormField
      id="username"
      label="Nom d'utilisateur"
      v-model="username"
      type="text"
      required
      :error-message="usernameErrorMessage"
    />

    <BaseFormField
      id="password"
      label="Mot de passe"
      v-model="password"
      type="password"
      required
      :error-message="passwordErrorMessage"
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
      <BaseButton v-else type="submit">Créer mon compte</BaseButton>
    </div>

    <div class="footer">
      <span class="footer-text">Vous avez déjà un compte ?</span>
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

.footer {
  text-align: center;
  padding-bottom: 30px;
}

.footer-text {
  color: rgb(100, 100, 100);
  font-size: 13px;
}

.footer-link {
  font-size: 16px;
  margin-left: 10px;
  color: rgb(20, 150, 250);
  text-decoration: none;
}

.footer-link:hover {
  text-decoration: underline;
  text-underline-offset: 2px;
}
</style>