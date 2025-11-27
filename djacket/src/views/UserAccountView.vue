<script setup lang="ts">
import { ref, onMounted } from "vue"
import { useRoute } from "vue-router"
import { useAuthStore } from "@/stores/auth"

const route = useRoute()
const auth = useAuthStore()

const showSuccessMessage = ref(false)

onMounted(() => {
  if (route.query.modified == "true") {
    showSuccessMessage.value = true
    setTimeout(() => showSuccessMessage.value = false, 4000)
  }
})
</script>

<template>
  <div class="content">

    <div v-if="showSuccessMessage" class="success-message">
      Modifications enregistrées avec succès.
    </div>

    <h1>Compte utilisateur</h1>

    <div class="user-info">Date de création du compte : {{ auth.user?.createdAt }}</div>
    <div class="user-info">Nom d'utilisateur : {{ auth.user?.username }}</div>
    <div class="user-info">Adresse e-mail : {{ auth.user?.email }}</div>
    <div class="user-info">
      Mot de passe : ************
      <RouterLink class="change-password-link" to="/change-password">Modifier</RouterLink>
    </div>

  </div>
</template>

<style scoped>
.content {
  padding-top: 30px;
  padding-bottom: 50px
}

.success-message {
  background-color: var(--color-success-light);
  color: var(--color-success);
  padding: 10px 15px;
  margin-bottom: 20px;
}

h1 {
  margin-bottom: 20px;
  color: var(--color-primary);
  font-size: 25px;
}

.user-info {
  margin-bottom: 15px;
  display: flex;
  align-items: center;
}

.change-password-link {
  font-size: 16px;
  margin-left: 10px;
  color: rgb(20, 150, 250);
  text-decoration: none;
}

.change-password-link:hover {
  text-decoration: underline;
  text-underline-offset: 2px;
}
</style>