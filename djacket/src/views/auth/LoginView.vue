<script setup lang="ts">
import { ref, watch } from "vue"
import { useRouter } from "vue-router"
import { useAuthStore } from "@/stores/auth"

import BaseForm from "@/components/BaseForm.vue"
import BaseInput from "@/components/BaseInput.vue"
import BaseInputPassword from "@/components/BaseInputPassword.vue"
import BaseLoadingSpinner from "@/components/BaseLoadingSpinner.vue"
import BaseButton from "@/components/BaseButton.vue"

const router = useRouter()
const authStore = useAuthStore()

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
    await authStore.login(email.value, password.value)
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

    <BaseInput
      v-model="email"
      id="email"
      type="email"
      label="Adresse e-mail"
      required
    />

    <BaseInputPassword
      v-model="password"
      id="password"
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
      <div class="footer-text">Vous n'avez pas encore de compte ?</div>
      <RouterLink class="footer-link" to="/signup">Créer mon compte</RouterLink>
      <div class="footer-text">Vous ne vous souvenez plus de votre mot de passe ?</div>
      <RouterLink class="footer-link" to="/reset-password">Mot de passe oublié</RouterLink>
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

.footer-text:last-of-type {
  margin-top: 15px;
}

.footer-link {
  font-size: 14px;
}
</style>
