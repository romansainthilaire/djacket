<script setup lang="ts">
import { ref, onMounted, nextTick, watch } from "vue"
import { useCartStore } from "@/stores/cart"
import { loadStripe } from "@stripe/stripe-js"
import api from "@/plugins/axios"

import BaseBreadcrumb from "@/components/base/BaseBreadcrumb.vue"
import BaseInput from "@/components/base/BaseInput.vue"
import BaseInputCheckbox from "@/components/base/BaseInputCheckbox.vue"
import BaseButton from "@/components/base/BaseButton.vue"

const cartStore = useCartStore()

const orderId = ref("")

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

const useSameAddress = ref(true)

const shippingFullNameError = ref("")
const shippingAddressLine1Error = ref("")
const shippingPostalCodeError = ref("")
const shippingCityError = ref("")
const shippingCountryError = ref("")

const billingFullNameError = ref("")
const billingAddressLine1Error = ref("")
const billingPostalCodeError = ref("")
const billingCityError = ref("")
const billingCountryError = ref("")

onMounted(async () => {
  stripe.value = await loadStripe("pk_test_51QV6q404TSsKpI2jt7YePW2642t5OfO7LtRIJ4YqlWQUgFfmfcIMd5zJG30NkugDcEAIA5Vl5WNYeJQmgnpv7RVP00VWlUJ2Y7")
})

function validateForm(): boolean {
  let isValid = true
  if (!shippingFullName.value) {
    shippingFullNameError.value = "Ce champ est obligatoire."
    isValid = false
  }
  if (!shippingAddressLine1.value) {
    shippingAddressLine1Error.value = "Ce champ est obligatoire."
    isValid = false
  }
  if (!shippingPostalCode.value) {
    shippingPostalCodeError.value = "Ce champ est obligatoire."
    isValid = false
  }
  if (!shippingCity.value) {
    shippingCityError.value = "Ce champ est obligatoire."
    isValid = false
  }
  if (!shippingCountry.value) {
    shippingCountryError.value = "Ce champ est obligatoire."
    isValid = false
  }
  if (!useSameAddress.value) {
    if (!billingFullName.value) {
      billingFullNameError.value = "Ce champ est obligatoire."
      isValid = false
    }
    if (!billingAddressLine1.value) {
      billingAddressLine1Error.value = "Ce champ est obligatoire."
      isValid = false
    }
    if (!billingPostalCode.value) {
      billingPostalCodeError.value = "Ce champ est obligatoire."
      isValid = false
    }
    if (!billingCity.value) {
      billingCityError.value = "Ce champ est obligatoire."
      isValid = false
    }
    if (!billingCountry.value) {
      billingCountryError.value = "Ce champ est obligatoire."
      isValid = false
    }
  }
  return isValid
}

async function checkout() {
  if (!validateForm()) {
    return
  }
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
      billingFullName: useSameAddress.value ? shippingFullName.value : billingFullName.value,
      billingAddressLine1: useSameAddress.value ? shippingAddressLine1.value : billingAddressLine1.value,
      billingAddressLine2: useSameAddress.value ? shippingAddressLine2.value : billingAddressLine2.value,
      billingPostalCode: useSameAddress.value ? shippingPostalCode.value : billingPostalCode.value,
      billingCity: useSameAddress.value ? shippingCity.value : billingCity.value,
      billingCountry: useSameAddress.value ? shippingCountry.value : billingCountry.value
    })
    orderId.value = response.data.order.id
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

async function cancelPayment() {
  loading.value = true
  errorMessage.value = ""
  try {
    if (orderId.value) {
      await api.delete(`orders/${orderId.value}/`)
      orderId.value = ""
    }
    if (stripePaymentElement.value) {
      stripePaymentElement.value.unmount()
      stripePaymentElement.value = null
    }
    stripeElements.value = null
  } catch (error) {
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

watch(useSameAddress, () => {
  billingFullName.value = ""
  billingAddressLine1.value = ""
  billingAddressLine2.value = ""
  billingPostalCode.value = ""
  billingCity.value = ""
  billingCountry.value = ""
  billingFullNameError.value = ""
  billingAddressLine1Error.value = ""
  billingPostalCodeError.value = ""
  billingCityError.value = ""
  billingCountryError.value = ""
})

watch(shippingFullName, () => {
  shippingFullNameError.value = ""
})

watch(shippingAddressLine1, () => {
  shippingAddressLine1Error.value = ""
})

watch(shippingPostalCode, () => {
  shippingPostalCodeError.value = ""
})

watch(shippingCity, () => {
  shippingCityError.value = ""
})

watch(shippingCountry, () => {
  shippingCountryError.value = ""
})

watch(billingFullName, () => {
  billingFullNameError.value = ""
})

watch(billingAddressLine1, () => {
  billingAddressLine1Error.value = ""
})

watch(billingPostalCode, () => {
  billingPostalCodeError.value = ""
})

watch(billingCity, () => {
  billingCityError.value = ""
})

watch(billingCountry, () => {
  billingCountryError.value = ""
})
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

    <div class="form-card">
      <div class="shipping-address-title-container">
        <p class="shipping-address-title">Adresse de livraison</p>
        <BaseButton
          class="shipping-address-edit-button"
          v-if="stripePaymentElement"
          @click="cancelPayment()"
          color="rgb(100, 100, 100)"
          bg-color="rgb(220, 220, 220)"
          bg-color-hover="rgb(220, 220, 220)"
          size="small"
          :disabled="loading"
        >
          Modifier
        </BaseButton>
      </div>
      <BaseInput
        id="shipping-full-name"
        type="text"
        v-model="shippingFullName"
        placeholder="Nom complet ou raison sociale"
        :disabled="!!stripePaymentElement"
        :error-message="shippingFullNameError"
      />
      <BaseInput
        id="shipping-address-line1"
        type="text"
        v-model="shippingAddressLine1"
        placeholder="Numéro et nom de la voie"
        :disabled="!!stripePaymentElement"
        :error-message="shippingAddressLine1Error"
      />
      <BaseInput
        id="shipping-address-line2"
        type="text"
        v-model="shippingAddressLine2"
        placeholder="Complément d'adresse"
        :disabled="!!stripePaymentElement"
      />
      <div class="postal-code-city-country">
        <BaseInput
          class="postal-code"
          id="shipping-postal-code"
          type="text"
          v-model="shippingPostalCode"
          placeholder="Code postal"
          :disabled="!!stripePaymentElement"
          :error-message="shippingPostalCodeError"
        />
        <BaseInput
          class="city"
          id="shipping-city"
          type="text"
          v-model="shippingCity"
          placeholder="Ville"
          :disabled="!!stripePaymentElement"
          :error-message="shippingCityError"
        />
        <BaseInput
          class="country"
          id="shipping-country"
          type="text"
          v-model="shippingCountry"
          placeholder="Pays"
          :disabled="!!stripePaymentElement"
          :error-message="shippingCountryError"
        />
      </div>
      <BaseInputCheckbox
        class="use-same-address-checkbox"
        label="L'adresse de facturation est identique à l'adresse de livraison."
        v-model="useSameAddress"
        :disabled="!!stripePaymentElement"
      />
      <template v-if="!useSameAddress">
        <div class="billing-address-title-container">
          <p class="billing-address-title">Adresse de facturation</p>
          <BaseButton
            class="billing-address-edit-button"
            v-if="stripePaymentElement"
            @click="cancelPayment()"
            color="rgb(100, 100, 100)"
            bg-color="rgb(220, 220, 220)"
            bg-color-hover="rgb(220, 220, 220)"
            size="small"
            :disabled="loading"
          >
            Modifier
          </BaseButton>
        </div>
        <BaseInput
          id="billing-full-name"
          type="text"
          v-model="billingFullName"
          placeholder="Nom complet ou raison sociale"
          :disabled="!!stripePaymentElement"
          :error-message="billingFullNameError"
        />
        <BaseInput
          id="billing-address-line1"
          type="text"
          v-model="billingAddressLine1"
          placeholder="Numéro et nom de la voie"
          :disabled="!!stripePaymentElement"
          :error-message="billingAddressLine1Error"
        />
        <BaseInput
          id="billing-address-line2"
          type="text"
          v-model="billingAddressLine2"
          placeholder="Complément d'adresse"
          :disabled="!!stripePaymentElement"
        />
        <div class="postal-code-city-country">
          <BaseInput
            class="postal-code"
            id="billing-postal-code"
            type="text"
            v-model="billingPostalCode"
            placeholder="Code postal"
            :disabled="!!stripePaymentElement"
            :error-message="billingPostalCodeError"
          />
          <BaseInput
            class="city"
            id="billing-city"
            type="text"
            v-model="billingCity"
            placeholder="Ville"
            :disabled="!!stripePaymentElement"
            :error-message="billingCityError"
          />
          <BaseInput
            class="country"
            id="billing-country"
            type="text"
            v-model="billingCountry"
            placeholder="Pays"
            :disabled="!!stripePaymentElement"
            :error-message="billingCountryError"
          />
        </div>
      </template>
    </div>

    <BaseButton
      v-if="!stripePaymentElement"
      class="checkout-button"
      @click="checkout()"
      :disabled="loading"
    >
      Passer au paiement
    </BaseButton>

    <div id="stripe-payment-element" v-show="stripePaymentElement"></div>
    
    <BaseButton
      class="confirm-payment-button"
      v-if="stripePaymentElement"
      @click="confirmPayment()"
      :disabled="loading"
    >
      Confirmer et payer
    </BaseButton>

    <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>

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

.summary-card,
.form-card {
  margin-top: 35px;
  border-radius: 8px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
  padding: 20px 15px;
}

.summary-title,
.shipping-address-title,
.billing-address-title {
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

.shipping-address-title-container,
.billing-address-title-container {
  display: flex;
  align-items: center;
  gap: 10px;
}

.postal-code-city-country {
  display: flex;
  gap: 20px;
}

.postal-code,
.city,
.country {
  flex: 1;
}

.use-same-address-checkbox {
  margin-top: 15px;
}

.billing-address-title-container {
  margin-top: 30px;
}

.checkout-button,
.confirm-payment-button {
  margin: auto;
  margin-top: 60px;
}

#stripe-payment-element {
  margin-top: 35px;
  border-radius: 8px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
  padding: 15px;
}

.error-message {
  margin-top: 20px;
  font-size: 13px;
  color: var(--color-error);
  text-align: center;
}

@media (max-width: 1100px) {
  .postal-code-city-country {
    flex-direction: column;
    gap: initial;
  }
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

  .shipping-address-title-container,
  .billing-address-title-container {
    flex-direction: column;
  }

  .checkout-button,
  .confirm-payment-button {
    margin-top: 40px;
  }
}
</style>