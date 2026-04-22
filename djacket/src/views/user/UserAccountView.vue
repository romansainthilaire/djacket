<script setup lang="ts">
import { ref, onMounted } from "vue"
import { useRoute, useRouter } from "vue-router"
import { useUserStore } from "@/stores/user"
import api from "@/plugins/axios"
import { formatDate } from "@/utils/format"

import BaseBreadcrumb from "@/components/base/BaseBreadcrumb.vue"
import BaseButton from "@/components/base/BaseButton.vue"
import BaseModal from "@/components/base/BaseModal.vue"
import BaseSvgIcon from "@/components/base/BaseSvgIcon.vue"

import eyeIcon from "@/assets/svg-icons/eye.svg?raw"

type Invoice = {
  id: number
  number: string
  createdAt: string
}

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()

const showSuccessMessage = ref(false)
const showDeleteAccountModal = ref(false)

const invoices = ref<Invoice[]>([])

onMounted(() => {
  if (route.query.modified == "true") {
    showSuccessMessage.value = true
    setTimeout(() => showSuccessMessage.value = false, 4000)
    const newQuery = { ...route.query }
    delete newQuery.modified
    router.replace({ query: newQuery })
  }
  fetchInvoices()
})

async function deleteAccount() {
  await userStore.deleteUser()
  showDeleteAccountModal.value = false
  router.push({ name: "login" })
}

async function fetchInvoices() {
  const response = await api.get("invoices/")
  invoices.value = response.data
}

async function viewInvoice(invoice: Invoice) {
  const response = await api.get(`invoices/${invoice.id}/url/`)
  const url = response.data.url
  window.open(url, "_blank")
}
</script>

<template>
  <div class="content">
    <BaseBreadcrumb
      :items="[
        { title: 'Accueil', to: '/' },
        { title: 'Espace utilisateur' }
      ]"
    />

    <div v-if="showSuccessMessage" class="success-message">
      Modifications enregistrées avec succès.
    </div>

    <h2 class="user-account-title">Votre compte</h2>

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

    <h2 class="user-invoices-title">Vos factures</h2>

    <table v-if="invoices.length">
      <thead>
        <tr>
          <th>Numéro de facture</th>
          <th>Date de création</th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="invoice in invoices" :key="invoice.id">
          <td>{{ invoice.number }}</td>
          <td>{{ formatDate(invoice.createdAt) }}</td>
          <td>
            <button class="view-button" @click="viewInvoice(invoice)">
              <BaseSvgIcon :svg="eyeIcon" color="white" width="22px" />
            </button>
          </td>
        </tr>
      </tbody>
    </table>

    <p v-else class="no-invoices">Aucune facture disponible.</p>

  </div>
</template>

<style scoped>
.content {
  padding-bottom: 100px
}

.success-message {
  background-color: var(--color-success-light);
  color: var(--color-success);
  padding: 10px 15px;
  margin: 20px 0;
}

.user-account-title,
.user-invoices-title {
  color: var(--color-primary);
  font-size: 25px;
}

.user-account-title {
  margin: 20px 0;
}

.user-invoices-title {
  margin-top: 40px;
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

table {
  border-collapse: collapse;
  margin-top: 25px;
  width: 100%;
  border-radius: 8px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
}

th, td {
  text-align: left;
  padding: 15px;
}

th {
  font-weight: 500;
}

td {
  border-top: 1px solid rgb(220, 220, 220);
}

td:last-child {
  text-align: right;
}

.view-button {
  background-color: var(--color-primary);
  border-radius: 4px;
  padding: 2px 3px 1px 3px;
}

.no-invoices {
  margin-top: 20px;
  font-style: italic;
}
</style>
