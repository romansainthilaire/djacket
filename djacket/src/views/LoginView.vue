<script setup lang="ts">
import { ref, watch } from "vue"
import { useRouter } from "vue-router"
import { useAuthStore } from "@/stores/auth"

import BaseForm from "@/components/BaseForm.vue"
import BaseFormField from "@/components/BaseFormField.vue"
import BaseLoadingSpinner from "@/components/BaseLoadingSpinner.vue"
import BaseButton from "@/components/BaseButton.vue"

const router = useRouter()
const auth = useAuthStore()

const email = ref("")
const password = ref("")

const invalidCredentialsError = ref(false)
const emailVerifiedError = ref(false)
const unknownError = ref(false)

const loading = ref(false)

function resetErrors() {
  invalidCredentialsError.value = false
  emailVerifiedError.value = false
  unknownError.value = false
}

async function login() {
  resetErrors()
  loading.value = true
  try {
    await auth.login(email.value, password.value)
    router.push({ name: "home" })
  } catch (error: any) {
    if (error.response?.data) {
      const data = error.response.data
      invalidCredentialsError.value = !!data.invalid_credentials
      emailVerifiedError.value = !!data.email_verified
    } else {
      unknownError.value = true
    }
  } finally {
    loading.value = false
  }
}

watch([email, password], () => {
  resetErrors()
})
</script>

<template>
  <BaseForm title="Connexion" @submit="login()">

    <BaseFormField
      v-model="email"
      id="email"
      type="email"
      label="Adresse e-mail"
      required
    />

    <BaseFormField
      v-model="password"
      id="password"
      type="password"
      label="Mot de passe"
      required
    />

    <p v-if="invalidCredentialsError" class="error-message">
      Nom d'utilisateur ou mot de passe incorrect.
    </p>

    <div v-if="emailVerifiedError" class="error-message">
      <p>Votre adresse e-mail n'a pas été vérifiée.</p>
      <p class="resend-message">
        Cliquez sur
        <RouterLink to="/resend-verification-email" class="resend-link">ce lien</RouterLink>
        pour renvoyer l'e-mail de vérification.
      </p>
    </div>
    
    <p v-if="unknownError" class="error-message">
      Une erreur est survenue. Veuillez réessayer plus tard.
    </p>

    <div class="submit-button-container">
      <BaseLoadingSpinner v-if="loading" />
      <BaseButton v-else type="submit">Me connecter</BaseButton>
    </div>

    <div class="footer">
      <span class="footer-text">Vous n'avez pas de compte ?</span>
      <RouterLink class="footer-link" to="/signup">Créer mon compte</RouterLink>
    </div>

  </BaseForm>
</template>

<style scoped>
.error-message {
  margin-top: 20px;
  font-size: 13px;
  color: var(--color-error);
}

.resend-message {
  margin-top: 5px;
}

.resend-link {
  color: var(--color-error);
  text-underline-offset: 2px;
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
