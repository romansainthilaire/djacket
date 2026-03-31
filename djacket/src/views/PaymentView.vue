<script setup lang="ts">
import { ref, onMounted, nextTick } from "vue"
import { useCartStore } from "@/stores/cart"
import { loadStripe } from "@stripe/stripe-js"
import api from "@/plugins/axios"

import BaseBreadcrumb from "@/components/base/BaseBreadcrumb.vue"

const cartStore = useCartStore()

const stripe = ref<any>(null)
const stripeElements = ref<any>(null)
const stripePaymentElement = ref<any>(null)

const loading = ref(false)
const errorMessage = ref("")

const shippingFullName = ref("")
const shippingAddressLine1 = ref("")
const shippingAddressLine2 = ref("")
const shippingPostalCode = ref("")
const shippingCity = ref("")
const shippingCountry = ref("")

const billingFullName = ref("")
const billingAddressLine1 = ref("")
const billingAddressLine2 = ref("")
const billingPostalCode = ref("")
const billingCity = ref("")
const billingCountry = ref("")

onMounted(async () => {
  stripe.value = await loadStripe("pk_test_51QV6q404TSsKpI2jt7YePW2642t5OfO7LtRIJ4YqlWQUgFfmfcIMd5zJG30NkugDcEAIA5Vl5WNYeJQmgnpv7RVP00VWlUJ2Y7")
})

async function checkout() {
  loading.value = true
  errorMessage.value = ""
  try {
    const response = await api.post("orders/checkout/", {
      items: cartStore.cart.map((item) => ({ product: item.product.id, quantity: item.quantity })),
      shippingFullName: shippingFullName.value,
      shippingAddressLine1: shippingAddressLine1.value,
      shippingAddressLine2: shippingAddressLine2.value,
      shippingPostalCode: shippingPostalCode.value,
      shippingCity: shippingCity.value,
      shippingCountry: shippingCountry.value,
      billingFullName: billingFullName.value,
      billingAddressLine1: billingAddressLine1.value,
      billingAddressLine2: billingAddressLine2.value,
      billingPostalCode: billingPostalCode.value,
      billingCity: billingCity.value,
      billingCountry: billingCountry.value
    })
    const clientSecret = response.data.clientSecret
    await nextTick()
    if (!stripePaymentElement.value) {
      stripeElements.value = stripe.value.elements({ clientSecret: clientSecret })
      stripePaymentElement.value = stripeElements.value.create("payment")
      stripePaymentElement.value.mount("#stripe-payment-element")
    }
  } catch (error) {
    errorMessage.value = "Erreur lors de la création du paiement."
  } finally {
    loading.value = false
  }
}

async function confirmPayment() {
  loading.value = true
  const { error } = await stripe.value.confirmPayment({
    elements: stripeElements.value,
    confirmParams: {
      return_url: "http://localhost:5173/payment-status"
    }
  })
  if (error) {
    errorMessage.value = error.message
  }
  loading.value = false
}
</script>

<template>
  <div class="content">
    <BaseBreadcrumb
      :items="[
        { title: 'Accueil', to: '/' },
        { title: 'Votre panier', to: '/cart' },
        { title: 'Paiement' }
      ]"
    />

    <h1>Votre commande</h1>

    <table>
      <thead>
        <tr>
          <th>Produit</th>
          <th>Prix</th>
          <th>Quantité</th>
          <th>Total</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in cartStore.cart" :key="item.product.id">
          <td>{{ item.product.name }}</td>
          <td data-label="Prix">{{ item.product.price.toFixed(2) }} €</td>
          <td data-label="Quantité">{{ item.quantity }}</td>
          <td data-label="Total">{{ (item.product.price * item.quantity).toFixed(2) }} €</td>
        </tr>
      </tbody>
    </table>

    <div class="summary-card">
      <p class="summary-title">Total de votre panier</p>
      <p class="summary-details">
        <span class="total-price">{{ cartStore.totalPrice.toFixed(2) }} €</span>
        ({{ cartStore.totalQuantity }} article{{ cartStore.totalQuantity > 1 ? "s" : "" }})
      </p>
    </div>

    <h2>Adresse de livraison</h2>

    <input v-model="shippingFullName" placeholder="Nom complet ou raison sociale" />
    <input v-model="shippingAddressLine1" placeholder="Numéro et nom de la voie" />
    <input v-model="shippingAddressLine2" placeholder="Complément d'adresse" />
    <input v-model="shippingPostalCode" placeholder="Code postal" />
    <input v-model="shippingCity" placeholder="Ville" />
    <input v-model="shippingCountry" placeholder="Pays" />

    <h2>Adresse de facturation</h2>

    <input v-model="billingFullName" placeholder="Nom complet ou raison sociale" />
    <input v-model="billingAddressLine1" placeholder="Numéro et nom de la voie" />
    <input v-model="billingAddressLine2" placeholder="Complément d'adresse" />
    <input v-model="billingPostalCode" placeholder="Code postal" />
    <input v-model="billingCity" placeholder="Ville" />
    <input v-model="billingCountry" placeholder="Pays" />

    <button @click="checkout()" :disabled="loading">Passer au paiement</button>

    <div v-if="stripePaymentElement">
      <h2>Paiement</h2>
      <div id="stripe-payment-element"></div>
      <button @click="confirmPayment()" :disabled="loading">Confirmer et payer</button>
    </div>

    <p v-if="errorMessage">{{ errorMessage }}</p>

  </div>
</template>

<style scoped>
.content {
  padding-bottom: 100px;
}

h1 {
  margin-top: 40px;
  color: var(--color-primary);
  font-size: 30px;
  font-weight: 500;
}

table {
  border-collapse: collapse;
  margin-top: 20px;
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

td:not(:first-child) {
  text-wrap: nowrap;
}

.summary-card {
  margin-top: 35px;
  border-radius: 8px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
  padding: 20px 15px;
}

.summary-title {
  font-size: 16px;
  font-weight: 500;
}

.summary-details {
  margin-top: 10px;
}

.total-price {
  font-weight: bold;
  color: var(--color-primary);
  margin-right: 5px;
}

@media (max-width: 600px) {
  .content {
    padding-bottom: 80px;
  }

  h1 {
    text-align: center;
    font-size: 25px;
    margin-top: 30px;
  }

  table {
    border-radius: none;
    box-shadow: none;
    margin-top: 30px;
  }

  thead {
    display: none;
  }

  tr {
    display: block;
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
    border-radius: 8px;
    margin-bottom: 35px;
  }

  td {
    display: flex;
    justify-content: space-between;
  }

  td::before {
    content: attr(data-label);
  }

  td:first-child {
    border-top: none;
    justify-content: center;
    text-align: center;
    font-weight: 500;
  }

  .summary-card {
    display: flex;
    flex-direction: column;
    align-items: center;
    margin-top: 0;
  }
}
</style>