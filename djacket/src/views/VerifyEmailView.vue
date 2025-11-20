<script setup lang="ts">
import { ref, onMounted } from "vue"
import { useRoute, useRouter } from "vue-router"
import { useAuthStore } from "@/stores/auth"

import BaseButton from "@/components/BaseButton.vue"

const route = useRoute()
const router = useRouter()
const auth = useAuthStore()

const loading = ref(true)
const email = ref("")
const errorMessage = ref("")
const emailVerified = ref(false)
const loadingResend = ref(false)

onMounted(async () => {
  const token = route.query.token as string
  if (!token) {
    loading.value = false
    return
  }
  try {
    const result = await auth.verifyEmail(token)
    if (result.verified) {
      email.value = result.email!
      emailVerified.value = true
    } else if (result.email) {
      email.value = result.email
      errorMessage.value = "Le lien de vérification a expiré."
    } else {
      errorMessage.value = "Le lien de vérification est invalide."
    }
  } catch {
    errorMessage.value = "Une erreur est survenue."
  } finally {
    loading.value = false
  }
})

async function resendVerificationEmail() {
  if (!email.value) {
    return
  }
  loadingResend.value = true
  try {
    await auth.resendVerificationEmail(email.value)
    router.push({ name: "verify-email-notice", params: { email: email.value } })
  } catch {
    errorMessage.value = "Une erreur est survenue lors de l'envoi de l'e-mail."
  } finally {
    loadingResend.value = false
  }
}

function goToLoginPage() {
  router.push({ name: "login" })
}

function goToSignupPage() {
  router.push({ name: "signup" })
}
</script>

<template>
  <div class="center">

    <div v-if="loading">Vérification...</div>

    <div v-else-if="loadingResend">Renvoi de l'e-mail...</div>

    <div v-else-if="emailVerified">
      <p>Votre adresse e-mail <b>{{ email }}</b> est vérifiée.</p>
      <p>Vous pouvez maintenant vous connecter.</p>
      <BaseButton @click="goToLoginPage()">Me connecter</BaseButton>
    </div>

    <div v-else>
      <p class="error">{{ errorMessage }}</p>
        <template v-if="email">
          <p>Renvoyer l'e-mail de vérification à <b>{{ email }}</b> ?</p>
          <BaseButton @click="resendVerificationEmail()">Renvoyer</BaseButton>       
        </template>
        <p>Recréer un compte avec une autre adresse e-mail ?</p>
        <BaseButton @click="goToSignupPage()">Recréer un compte</BaseButton>
    </div>

  </div>
</template>