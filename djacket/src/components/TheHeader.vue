<script setup lang="ts">
import { ref } from "vue"
import { useRouter } from "vue-router"
import { useAuthStore } from "@/stores/auth"

import BaseSvgIcon from "./BaseSvgIcon.vue"
import BaseModal from "./BaseModal.vue"

import menuIcon from "@/assets/svg-icons/menu.svg?raw"
import userIcon from "@/assets/svg-icons/user.svg?raw"
import logoutIcon from "@/assets/svg-icons/logout.svg?raw"


const router = useRouter()
const auth = useAuthStore()

const isOpen = ref(false)
const showLogoutModal = ref(false)

function toggleMenu() {
  isOpen.value = !isOpen.value
}

function logout() {
  auth.logout()
  router.push("/login")
}
</script>

<template>
  <header>
    <div class="content">

      <div class="top">
        <div class="logo">Djacket</div>
        <button class="menu-button" @click="toggleMenu()">
          <BaseSvgIcon :svg="menuIcon" color="white" />
        </button>
      </div>

      <nav :class="{ 'open': isOpen }">
        <div class="nav-links">
          <RouterLink class="nav-link" to="/">Accueil</RouterLink>
          <RouterLink class="nav-link" to="/about">À propos</RouterLink>
        </div>
        <div class="auth" :class="{ 'logged-in': auth.user }">
          <template v-if="auth.user">
            <RouterLink class="nav-link" to="/user-account">
              <BaseSvgIcon class="user-icon" :svg="userIcon" color="white" width="25px" />
              {{ auth.user.username }}
            </RouterLink>
            <button class="logout-button" @click="showLogoutModal = true">
              <BaseSvgIcon :svg="logoutIcon" color="var(--color-primary)" width="25px" />
            </button>
          </template>
          <RouterLink v-else class="login-button" to="/login">Connexion</RouterLink>
        </div>
      </nav>

      <BaseModal
        v-if="showLogoutModal"
        title="Déconnexion"
        text="Êtes-vous sûr de vouloir vous déconnecter ?"
        show-confirm-button
        @close="showLogoutModal = false"
        @confirm="logout()"
      />

    </div>
  </header>
</template>

<style scoped>
header {
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: var(--color-primary);
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

.auth {
  display: flex;
  align-items: center;
}

.auth > .nav-link {
  display: flex;
  align-items: center;
}

.user-icon {
  margin-right: 5px;
}

.logout-button {
  background-color: white;
  border-radius: 4px;
  padding: 3px;
  margin-left: 10px;
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

  .auth.logged-in {
    margin: 10px 0;
  }

  .logout-button {
    margin-left: 20px;
  }
}
</style>
