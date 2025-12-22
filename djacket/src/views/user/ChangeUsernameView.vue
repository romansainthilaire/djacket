<script setup lang="ts">
import { ref, watch } from "vue"
import { useRouter } from "vue-router"
import { useUserStore } from "@/stores/user"

import BaseBreadcrumb from "@/components/base/BaseBreadcrumb.vue"
import BaseForm from "@/components/base/BaseForm.vue"
import BaseInput from "@/components/base/BaseInput.vue"
import BaseLoadingSpinner from "@/components/base/BaseLoadingSpinner.vue"
import BaseButton from "@/components/base/BaseButton.vue"

const router = useRouter()
const userStore = useUserStore()

const username = ref("")
const loading = ref(false)

const usernameErrorMessage = ref("")
const unknownErrorMessage = ref("")

async function changeUsername() {
  unknownErrorMessage.value = ""
  loading.value = true
  try {
    await userStore.editUser({ username: username.value })
    router.push({ name: "user-account", query: { modified: "true" } })
  } catch (error: any) {
    if (error.response?.data) {
      const data = error.response.data
      usernameErrorMessage.value = data.username ? data.username.join(" ") : ""
    } else {
      unknownErrorMessage.value = "Une erreur est survenue. Veuillez réessayer plus tard."
    }
  } finally {
    loading.value = false
  }
}

watch(username, () => {
  usernameErrorMessage.value = ""
  unknownErrorMessage.value = ""
})
</script>

<template>
  <BaseBreadcrumb
    :items="[
      { title: 'Compte utilisateur', to: '/user-account' },
      { title: 'Modification du nom d\'utilisateur' }
    ]"
  />

  <BaseForm title="Modification du nom d'utilisateur" @submit="changeUsername()">

    <p class="intro">
      Votre nom d'utilisateur actuel est : <b>{{ userStore.user?.username }}</b>
    </p>

    <BaseInput
      v-model="username"
      id="username"
      type="text"
      label="Nouveau nom d'utilisateur"
      required
      :error-message="usernameErrorMessage"
    />

    <p v-if="unknownErrorMessage" class="error-message">{{ unknownErrorMessage }}</p>

    <div class="submit-button-container">
      <BaseLoadingSpinner v-if="loading" />
      <BaseButton v-else type="submit">Enregistrer</BaseButton>
    </div>

  </BaseForm>
</template>

<style scoped>
.intro {
  margin-top: 30px;
}

.error-message {
  margin-top: 15px;
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
