<script setup lang="ts">
import { ref, computed, watch } from "vue"
import { useRouter } from "vue-router"
import { useAuthStore } from "@/stores/auth"

import BaseLoadingSpinner from "@/components/BaseLoadingSpinner.vue"
import BaseButton from "@/components/BaseButton.vue"

const router = useRouter()
const auth = useAuthStore()

const email = ref("")
const loading = ref(false)
const error = ref(false)

const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
const emailIsValid = computed(() => emailRegex.test(email.value.trim()))

async function resendEmail() {
  if (!emailIsValid.value) {
    return
  }
  loading.value = true
  try {
    await auth.resendVerificationEmail(email.value)
    router.push({ name: "verify-email-notice", params: { email: email.value } })
  } catch {
    error.value = true
  } finally {
    loading.value = false
  }
}

watch(email, () => {
  error.value = false
})
</script>

<template>
  <div class="content">
  
    <div v-if="loading" class="loading-container">
      <BaseLoadingSpinner />
      <div class="loading-text">Envoi en cours...</div>
    </div>

    <div v-else>
      <h1>Renvoyer l'e-mail de vérification</h1>

      <p>Entrez votre adresse e-mail pour recevoir un nouvel e-mail de vérification :</p>

      <form @submit.prevent="resendEmail()">
        <div class="form-field">
          <label for="email">Adresse e-mail</label>
          <input v-model="email" id="email" type="email" required />
        </div>
        <BaseButton type="submit" :disabled="!emailIsValid">Renvoyer</BaseButton>
      </form>

      <p v-if="error" class="error-message">
        Impossible de renvoyer l'e-mail. Veuillez réessayer plus tard.
      </p>
    </div>

  </div>
</template>

<style scoped>
.content {
  padding-top: 30px;
  padding-bottom: 50px
}

.loading-container {
  text-align: center;
}

.loading-text {
  margin-top: 10px;
}

h1 {
  margin-bottom: 10px;
  color: var(--color-primary);
  font-size: 25px;
}

.form-field {
  display: flex;
  flex-direction: column;
  margin-top: 15px;
  margin-bottom: 25px;
}

label {
  margin-bottom: 5px;
  font-size: 16px;
}

input {
  max-width: 400px;
  padding: 10px;
  border: none;
  border-radius: 4px;
  outline: 1px solid rgb(200, 200, 200);
  color: var(--color-primary);
  font-size: 16px;
}

input:focus {
  outline: 1px solid var(--color-primary);
}

.error-message {
  margin-top: 15px;
  color: var(--color-error);
}
</style>
