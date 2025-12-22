<script setup lang="ts">
import { useRouter, RouterView } from "vue-router"
import { useUserStore } from "@/stores/user"

import TheHeader from "@/components/layout/TheHeader.vue"
import TheFooter from "@/components/layout/TheFooter.vue"
import BaseModal from "@/components/base/BaseModal.vue"
import BaseButton from "@/components/base/BaseButton.vue"

const router = useRouter()
const userStore = useUserStore()

function goToChangePasswordPage() {
  router.push({ name: "change-password" })
}
</script>

<template>
  <div class="app-layout">
    <TheHeader />
    <main>
      <div class="app-content">
        <RouterView />
      </div>
    </main>
    <TheFooter />
    <BaseModal
      v-if="userStore.user?.mustChangePassword && router.currentRoute.value.name != 'change-password'"
      title="Action requise"
    >
      <p>Pour sécuriser votre compte, vous devez changer votre mot de passe maintenant.</p>
      <div class="change-password-button-container">
        <BaseButton @click="goToChangePasswordPage()">J'ai compris</BaseButton>
      </div>
    </BaseModal>
  </div>
</template>

<style scoped>
.app-layout {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

main {
  flex: 1;
  display: flex;
  justify-content: center;
}

.app-content {
  width: 100%;
  max-width: 1000px;
  padding: 0 20px;
}

.change-password-button-container {
  margin-top: 30px;
  display: flex;
  justify-content: center;
}
</style>
