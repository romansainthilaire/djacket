<script setup lang="ts">
import { RouterLink, RouterView } from "vue-router"
import TheHeader from "@/components/TheHeader.vue"
import TheFooter from "@/components/TheFooter.vue"
import HelloWorld from "@/components/HelloWorld.vue"
</script>

<template>
  <div class="layout">
    <TheHeader />
    <main class="content">
      <img alt="Vue logo" src="@/assets/logo.svg" width="125" height="125" />
      <HelloWorld />
      <RouterLink to="/">Home</RouterLink>
      <RouterLink to="/about">About</RouterLink>
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
