<script setup lang="ts">
import { ref } from "vue"
import { useRouter } from "vue-router"
import { useUserStore } from "@/stores/user"
import { useCartStore } from "@/stores/cart"
import type { Item } from "@/stores/cart"

import BaseBreadcrumb from "@/components/base/BaseBreadcrumb.vue"
import BaseModal from "@/components/base/BaseModal.vue"
import BaseSvgIcon from "@/components/base/BaseSvgIcon.vue"
import BaseButton from "@/components/base/BaseButton.vue"

import addIcon from "@/assets/svg-icons/add.svg?raw"
import removeIcon from "@/assets/svg-icons/remove.svg?raw"

const router = useRouter()
const userStore = useUserStore()
const cartStore = useCartStore()

const itemToRemove = ref<Item | null>(null)

function goToPaymentPage() {
  router.push({ name: "payment" })
}
</script>

<template>
  <div class="content">
    <BaseBreadcrumb
      :items="[
        { title: 'Accueil', to: '/' },
        { title: 'Votre panier' }
      ]"
    />

    <h1>Votre panier</h1>

    <template v-if="cartStore.totalQuantity == 0">
      <p class="empty-cart-message">
        Vous n'avez aucun article dans votre panier.
      </p>
    </template>

    <template v-else>

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
            <td data-label="Quantité">
              <div class="quantity">
                {{ item.quantity }}
                <button
                  class="remove-button"
                  @click="item.quantity > 1 ? cartStore.decreaseQuantity(item) : itemToRemove = item"
                >
                  <BaseSvgIcon :svg="removeIcon" color="white" width="16px" />
                </button>
                <button
                  class="add-button"
                  @click="cartStore.increaseQuantity(item)"
                >
                  <BaseSvgIcon :svg="addIcon" color="white" width="16px" />
                </button>
              </div>
            </td>
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
        <p class="login-required-message" v-if="!userStore.user">
          Vous devez être connecté pour finaliser votre commande.
        </p>
        <BaseButton @click="goToPaymentPage()">Finaliser ma commande</BaseButton>
      </div>

      <BaseModal
        v-if="itemToRemove"
        :title="itemToRemove.product.name"
        text="Voulez-vous retirer ce produit du panier ?"
        show-close-button
        show-confirm-button
        @close="itemToRemove = null"
        @confirm="cartStore.removeFromCart(itemToRemove)"
      />

    </template>

  </div>
</template>

<style scoped>
.content {
  padding-bottom: 100px;
}

h1 {
  margin-top: 30px;
  color: var(--color-primary);
  font-size: 30px;
  font-weight: 500;
}

.empty-cart-message {
  margin-top: 20px;
  color: rgb(100, 100, 100);
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

.remove-button,
.add-button {
  background-color: rgb(200, 200, 200);
  border-radius: 50%;
  padding: 2px;
  margin-left: 7px;
}

.quantity {
  display: flex;
  align-items: center;
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
  margin-bottom: 30px;
}

.login-required-message {
  color: rgb(100, 100, 100);
  font-size: 14px;
  margin-bottom: 10px;
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
    margin-top: 20px;
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

  .login-required-message {
    text-align: center;
    margin-bottom: 15px;
  }
}
</style>