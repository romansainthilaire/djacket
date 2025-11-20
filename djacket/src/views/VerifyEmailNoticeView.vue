<script setup lang="ts">
const props = defineProps<{
  email: string
}>()
</script>

<template>
  <div>
    <h1>Vérification requise</h1>
    <p>Un e-mail a été envoyé à <b>{{ email }}</b>. Cliquez sur le lien pour activer votre compte (valide 24h).</p>
  </div>
</template>