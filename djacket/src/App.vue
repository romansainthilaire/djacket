<script setup lang="ts">
import { RouterLink, RouterView } from "vue-router"
import TheHeader from "@/components/TheHeader.vue"
import TheFooter from "@/components/TheFooter.vue"
</script>

<template>
  <div class="layout">
    <TheHeader />
    <main class="content">
      <RouterView />
    </main>
    <TheFooter />
  </div>
</template>

<style scoped>
.layout {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.content {
  flex: 1;
}
</style>
