<script setup lang="ts">
import { ref, onMounted } from "vue"
import { useRoute, useRouter } from "vue-router"
import { useUserStore } from "@/stores/user"
import { formatDate } from "@/utils/format"

import BaseButton from "@/components/BaseButton.vue"
import BaseModal from "@/components/BaseModal.vue"


const route = useRoute()
const router = useRouter()
const userStore = useUserStore()

const showSuccessMessage = ref(false)
const showDeleteAccountModal = ref(false)

onMounted(() => {
  if (route.query.modified == "true") {
    showSuccessMessage.value = true
    setTimeout(() => showSuccessMessage.value = false, 4000)
    const newQuery = { ...route.query }
    delete newQuery.modified
    router.replace({ query: newQuery })
  }
})

async function deleteAccount() {
  await userStore.deleteUser()
  showDeleteAccountModal.value = false
  router.push({ name: "login" })
}
</script>

<template>
  <div class="content">

    <div v-if="showSuccessMessage" class="success-message">
      Modifications enregistrées avec succès.
    </div>

    <h1>Compte utilisateur</h1>

    <div class="user-info">Date de création du compte : {{ formatDate(userStore.user?.createdAt) }}</div>
    <div class="user-info">
      Nom d'utilisateur : {{ userStore.user?.username }}
      <RouterLink class="change-username-link" to="/user-account/change-username">Modifier</RouterLink>
    </div>
    <div class="user-info">Adresse e-mail : {{ userStore.user?.email }}</div>
    <div class="user-info">
      Mot de passe : ************
      <RouterLink class="change-password-link" to="/user-account/change-password">Modifier</RouterLink>
    </div>

    <BaseButton
      class="delete-account-button"
      size="small"
      bg-color="var(--color-error)"
      bg-color-hover="var(--color-error)"
      @click="showDeleteAccountModal = true"
    >
      Supprimer mon compte
    </BaseButton>

    <BaseModal
      v-if="showDeleteAccountModal"
      title="Suppression de compte"
      show-close-button
      @close="showDeleteAccountModal = false"
    >
      <div class="delete-account-modal-content">
        <p class="warning-emoji">⚠️</p>
        <p><strong>La suppression de votre compte est irréversible.</strong></p>
        <p>Toutes les données associées seront perdues.</p>
        <p>Êtes-vous sûr de vouloir continuer ?</p>
        <BaseButton
          class="delete-account-modal-button"
          bg-color="var(--color-error)"
          bg-color-hover="var(--color-error)"
          @click="deleteAccount()"
        >
          Confirmer la suppression
        </BaseButton>
      </div>
    </BaseModal>

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

.delete-account-button {
  margin-top: 30px;
}

.delete-account-modal-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.warning-emoji {
  font-size: 40px;
  line-height: 40px;
  margin-bottom: 25px;
}

.delete-account-modal-content :not(:first-child):not(:last-child) {
  margin-bottom: 10px;
}

.delete-account-modal-button {
  margin-top: 20px;
}
</style>
