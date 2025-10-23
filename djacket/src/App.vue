<script setup lang="ts">
import { RouterLink, RouterView } from "vue-router"
import HelloWorld from "./components/HelloWorld.vue"
</script>

<template>

  <img alt="Vue logo" src="@/assets/logo.svg" width="125" height="125" />

  <HelloWorld />

  <RouterLink to="/">Home</RouterLink>
  <RouterLink to="/about">About</RouterLink>

  <RouterView />
</template>

<style scoped>
</style>
