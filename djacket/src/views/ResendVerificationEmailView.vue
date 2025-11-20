<script setup lang="ts">
import { ref } from "vue"
import { useAuthStore } from "@/stores/auth"

import BaseButton from "@/components/BaseButton.vue"

const auth = useAuthStore()

const email = ref("")
const loading = ref(false)
const successMessage = ref("")
const errorMessage = ref("")

async function resendEmail() {
  if (!email.value) {
    return
  }
  loading.value = true
  errorMessage.value = ""
  successMessage.value = ""
  try {
    await auth.resendVerificationEmail(email.value)
    successMessage.value = "E-mail de vérification renvoyé. Pensez à vérifier vos spams."
  } catch {
    errorMessage.value = "Impossible de renvoyer l'e-mail. Veuillez réessayer."
  } finally {
    loading.value = false
  }
}
</script>

<template>

  <h1>Renvoyer l'e-mail de vérification</h1>

  <div v-if="loading">Envoi en cours...</div>

  <div v-else>
    <p>Entrez votre adresse e-mail pour recevoir un nouvel e-mail de vérification :</p>
    <label for="email">Adresse e-mail</label>
    <input v-model="email" id="email" type="email" autofocus />
    <BaseButton @click="resendEmail()" :disabled="!email">Renvoyer</BaseButton>
    <p v-if="successMessage">{{ successMessage }}</p>
    <p v-if="errorMessage">{{ errorMessage }}</p>
  </div>
  
</template>
