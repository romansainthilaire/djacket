<script setup lang="ts">
import { ref, computed, watch } from "vue"
import { useRouter } from "vue-router"
import { useAuthStore } from "@/stores/auth"

import BaseForm from "@/components/BaseForm.vue"
import BaseInput from "@/components/BaseInput.vue"
import BaseLoadingSpinner from "@/components/BaseLoadingSpinner.vue"
import BaseButton from "@/components/BaseButton.vue"

const router = useRouter()
const auth = useAuthStore()

const email = ref("")
const loading = ref(false)
const error = ref(false)

const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
const emailIsValid = computed(() => emailRegex.test(email.value.trim()))

async function resetPassword() {
  if (!emailIsValid.value) {
    return
  }
  loading.value = true
  try {
    await auth.resetPassword(email.value)
    router.push({ name: "reset-password-notice", params: { email: email.value } })
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
  <BaseForm title="Réinitialisation du mot de passe" @submit="resetPassword()">

    <p class="intro">
      Entrez votre adresse e-mail pour recevoir un mot de passe temporaire :
    </p>
    
    <BaseInput
      v-model="email"
      id="email"
      type="email"
      label="Adresse e-mail"
      required
    />

    <p v-if="error" class="error-message">
      Impossible d'envoyer l'e-mail. Veuillez réessayer plus tard.
    </p>

    <div class="submit-button-container">
      <BaseLoadingSpinner v-if="loading" />
      <BaseButton v-else type="submit" :disabled="!emailIsValid">Envoyer</BaseButton>
    </div>

  </BaseForm>
</template>

<style scoped>
.intro {
  margin-top: 30px;
}

.error-message {
  margin-top: 20px;
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
