<script setup lang="ts">
import { ref, onMounted } from "vue"
import { useCartStore } from "@/stores/cart"
import { loadStripe } from "@stripe/stripe-js"

import BaseLoadingSpinner from "@/components/base/BaseLoadingSpinner.vue"
import BaseButton from "@/components/base/BaseButton.vue"

type PaymentStatus =
  "succeeded"
  | "processing"
  | "requires_action"
  | "requires_payment_method"
  | "canceled"

const cartStore = useCartStore()

const loading = ref(true)
const stripe = ref<any>(null)
const status = ref<PaymentStatus | "">("")
const errorMessage = ref("")

onMounted(async () => {
  stripe.value = await loadStripe("pk_test_51QV6q404TSsKpI2jt7YePW2642t5OfO7LtRIJ4YqlWQUgFfmfcIMd5zJG30NkugDcEAIA5Vl5WNYeJQmgnpv7RVP00VWlUJ2Y7")
  const urlParams = new URLSearchParams(window.location.search)
  const clientSecret = urlParams.get("payment_intent_client_secret")
  try {
    const response = await stripe.value.retrievePaymentIntent(clientSecret)
    const paymentIntent = response.paymentIntent
    status.value = paymentIntent.status
    if (status.value == "succeeded") {
      cartStore.clear()
    }
  } catch (error: any) {
    errorMessage.value = "Erreur lors de la vérification du paiement."
  } finally {
    loading.value = false
  }
})

function reload() {
  window.location.reload()
}
</script>

<template>
  <div class="content">

    <BaseLoadingSpinner v-if="loading" text="Chargement..." />

    <template v-else>

      <h1>Confirmation du paiement</h1>

      <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>

      <div v-else-if="status == 'succeeded'">
        <p>✅ Paiement effectué avec succès.</p>
        <p class="find-invoices">
          Retrouvez toutes
          <RouterLink to="/user-account">vos factures</RouterLink>
          dans votre espace utilisateur.
        </p>
      </div>

      <div v-else-if="['processing', 'requires_action'].includes(status)">
        <p>⏳ Paiement en cours de traitement...</p>
        <BaseButton @click="reload()" class="reload-button">Rafraîchir la page</BaseButton>
      </div>

      <div v-else-if="['requires_payment_method', 'canceled'].includes(status)">
        <p>❌ Le paiement a échoué.</p>
      </div>

      <div v-else>
        <p>⚠️ Statut de paiement inconnu : {{ status }}</p>
      </div>

    </template>

  </div>
</template>

<style scoped>
.content {
  margin-top: 30px;
}

h1 {
  font-size: 25px;
  color: var(--color-primary);
  margin-bottom: 15px;
}

.error-message {
  font-size: 13px;
  color: var(--color-error);
}

.find-invoices {
  margin-top: 10px;
}

.reload-button {
  margin-top: 40px;
}
</style>