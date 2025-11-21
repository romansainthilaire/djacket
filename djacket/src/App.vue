<script setup lang="ts">
import { RouterView } from "vue-router"
import TheHeader from "@/components/TheHeader.vue"
import TheFooter from "@/components/TheFooter.vue"
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
</style>
