<script setup lang="ts">
import { ref, onMounted } from "vue"
import { useRoute, useRouter } from "vue-router"
import { useAuthStore } from "@/stores/auth"
import { formatDate } from "@/utils/format"

const route = useRoute()
const router = useRouter()
const auth = useAuthStore()

const showSuccessMessage = ref(false)

onMounted(() => {
  if (route.query.modified == "true") {
    showSuccessMessage.value = true
    setTimeout(() => showSuccessMessage.value = false, 4000)
    const newQuery = { ...route.query }
    delete newQuery.modified
    router.replace({ query: newQuery })
  }
})
</script>

<template>
  <div class="content">

    <div v-if="showSuccessMessage" class="success-message">
      Modifications enregistrées avec succès.
    </div>

    <h1>Compte utilisateur</h1>

    <div class="user-info">Date de création du compte : {{ formatDate(auth.user?.createdAt) }}</div>
    <div class="user-info">
      Nom d'utilisateur : {{ auth.user?.username }}
      <RouterLink class="change-username-link" to="/user-account/change-username">Modifier</RouterLink>
    </div>
    <div class="user-info">Adresse e-mail : {{ auth.user?.email }}</div>
    <div class="user-info">
      Mot de passe : ************
      <RouterLink class="change-password-link" to="/user-account/change-password">Modifier</RouterLink>
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

.change-username-link,
.change-password-link {
  font-size: 14px;
  margin-left: 10px;
}
</style>
