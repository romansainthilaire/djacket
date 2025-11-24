<script setup lang="ts">
import { ref } from "vue"
import { useAuthStore } from "@/stores/auth"

const auth = useAuthStore()
const isOpen = ref<boolean>(false)

const toggleMenu = () => {
  isOpen.value = !isOpen.value
}
</script>

<template>
  <header>
    <div class="content">

      <div class="top">
        <div class="logo">Djacket</div>
        <button class="menu-button" @click="toggleMenu()">
          <img src="@/assets/menu.svg" alt="Menu" />
        </button>
      </div>

      <nav :class="{ 'open': isOpen }">
        <div class="nav-links">
          <RouterLink class="nav-link" to="/">Accueil</RouterLink>
          <RouterLink class="nav-link" to="/about">À propos</RouterLink>
        </div>
        <div class="auth">
          <template v-if="auth.user">{{ auth.user.username }}</template>
          <RouterLink v-else class="login-button" to="/login">Connexion</RouterLink>
        </div>
      </nav>

    </div>
  </header>
</template>

<style scoped>
header {
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: rgb(0, 0, 140);
  height: 65px;
}

.content {
  display: flex;
  align-items: center;
  width: 100%;
  max-width: 1000px;
  padding: 0 20px;
}

.logo {
  color: white;
  font-size: 23px;
  font-family: "Fjalla One", sans-serif;
  margin-right: 20px;
}

.menu-button {
  display: none;
  background: none;
  padding: 0;
  line-height: 0;
}

nav {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
}

.nav-link {
  color: white;
  text-decoration: none;
  font-size: 16px;
  padding: 6px 12px;
  border-radius: 4px;
  margin: 0 5px;
  transition: background-color 0.3s ease;
}

.nav-link:hover {
  background-color: rgba(255, 255, 255, 0.15);
}

.login-button {
  color: white;
  text-decoration: none;
  font-size: 16px;
  padding: 6px 12px;
  border-radius: 4px;
  background-color: rgb(0, 140, 140);
  transition: background-color 0.3s ease;
}

.login-button:hover {
  background-color: rgb(0, 160, 160);
}

@media (max-width: 600px) {
  header {
    height: auto;
  }

  .content {
    flex-direction: column;
    padding: 10px 20px;
  }

  .top {
    display: flex;
    align-items: center;
    justify-content: space-between;
    width: 100%;
  }

  .menu-button {
    display: block;
  }

  nav {
    display: none;
  }

  nav.open {
    display: flex;
    align-items: start;
    flex-direction: column;
  }

  .nav-links {
    display: flex;
    flex-direction: column;
  }

  .nav-link {
    margin: 8px 0;
    padding: 0;
  }

  .nav-link:hover {
    background-color: initial;
  }

  .auth {
    margin: 20px 0;
  }
}
</style>
