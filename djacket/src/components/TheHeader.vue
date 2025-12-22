<script setup lang="ts">
import { ref } from "vue"
import { useRouter } from "vue-router"
import { useAuthStore } from "@/stores/auth"
import { useUserStore } from "@/stores/user"

import BaseSvgIcon from "./base/BaseSvgIcon.vue"
import BaseModal from "./base/BaseModal.vue"
import HeaderNavDropdown from "./HeaderNavDropdown.vue"

import menuIcon from "@/assets/svg-icons/menu.svg?raw"
import userIcon from "@/assets/svg-icons/user.svg?raw"
import logoutIcon from "@/assets/svg-icons/logout.svg?raw"


const router = useRouter()
const authStore = useAuthStore()
const userStore = useUserStore()

const isOpen = ref(false)
const showLogoutModal = ref(false)

function toggleMenu() {
  isOpen.value = !isOpen.value
}

function logout() {
  authStore.logout()
  router.push({ name: "login" })
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
          <HeaderNavDropdown
            name="Collections"
            :links="[
              { text: 'Hiver', to: '/collections/hiver' },
              { text: 'Été', to: '/collections/ete' },
              { text: 'Automne', to: '/collections/automne' },
              { text: 'Printemps', to: '/collections/printemps' }
            ]"
          />
        </div>
        <div class="auth" :class="{ 'logged-in': userStore.user }">
          <template v-if="userStore.user">
            <RouterLink class="nav-link" to="/user-account">
              <BaseSvgIcon class="user-icon" :svg="userIcon" color="white" width="25px" />
              {{ userStore.user.username }}
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
        show-close-button
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
    background-color: transparent;
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
