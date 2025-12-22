<script setup lang="ts">
import { useRouter } from "vue-router"

import BaseButton from "@/components/base/BaseButton.vue"

const props = defineProps<{
  email: string
}>()

const router = useRouter()

function goToLoginPage() {
  router.push({ name: "login" })
}
</script>

<template>
  <h1>Réinitialisation en cours</h1>
  <p>Un mot de passe temporaire a été envoyé à : <b>{{ props.email }}</b></p>
  <p>👉 Pensez à vérifier votre dossier spam.</p>
  <BaseButton @click="goToLoginPage()">Me connecter</BaseButton>
</template>

<style scoped>
h1 {
  margin-top: 30px;
  margin-bottom: 10px;
  color: var(--color-primary);
  font-size: 25px;
}

p {
  margin-bottom: 5px;
}

button {
  margin-top: 20px;
}
</style>
