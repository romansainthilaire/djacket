<script setup lang="ts">
import { ref, watch } from "vue"
import { useRouter } from "vue-router"
import { useAuthStore } from "@/stores/auth"

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
  <div class="content">
    <div class="card">

      <div class="header">
        <h1>Connexion</h1>
      </div>

      <form @submit.prevent="login()">

        <div class="form-field">
          <label for="email">Adresse e-mail</label>
          <input v-model="email" id="email" type="email" required />
        </div>

        <div class="form-field">
          <label for="password">Mot de passe</label>
          <input v-model="password" id="password" type="password" required />
        </div>

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

      </form>

      <div class="footer">
        <span class="footer-text">Vous n'avez pas de compte ?</span>
        <RouterLink class="footer-link" to="/signup">Créer mon compte</RouterLink>
      </div>

    </div>
  </div>
</template>

<style scoped>
.content {
  display: flex;
  justify-content: center;
  padding-top: 60px;
  padding-bottom: 100px;
}

.card {
  width: 100%;
  max-width: 450px;
  border-radius: 8px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
}

.header {
  height: 80px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: rgb(245, 245, 255);
}

h1 {
  color: rgb(0, 0, 140);
  font-size: 25px;
  font-weight: 600;
}

form {
  padding: 0 30px;
}

.form-field {
  display: flex;
  flex-direction: column;
  margin-top: 20px;
}

label {
  margin-bottom: 5px;
  font-size: 16px;
}

input {
  width: 100%;
  box-sizing: border-box;
  padding: 10px;
  border: none;
  border-radius: 4px;
  outline: 1px solid rgb(200, 200, 200);
  color: rgb(0, 0, 140);
  font-size: 16px;
}

input:focus {
  outline: 1px solid rgb(0, 0, 140);
}

.error-message {
  margin-top: 20px;
  font-size: 13px;
  color: rgb(220, 20, 80);
}

.resend-message {
  margin-top: 5px;
}

.resend-link {
  color: rgb(220, 20, 80);
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

@media (max-width: 600px) {
  .content {
    padding-top: 0;
    padding-bottom: 50px;
  }

  .header {
    margin-left: -20px;
    margin-right: -20px;
  }

  form {
    padding: 0;
  }

  .card {
    max-width: none;
    border-radius: 0;
    box-shadow: none;
  }
}
</style>
