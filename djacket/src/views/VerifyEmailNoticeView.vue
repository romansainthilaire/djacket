<script setup lang="ts">
const props = defineProps<{
  email: string
}>()
</script>

<template>
  <h1>Vérification requise</h1>
  <p>Un e-mail de vérification a été envoyé à : <b>{{ props.email }}</b></p>
  <p>Cliquez sur le lien reçu pour activer votre compte (valide 24h).</p>
  <p>👉 Pensez à vérifier votre dossier spam.</p>
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
</style>
