<script setup lang="ts">
import { useCartStore } from "@/stores/cart"

import BaseBreadcrumb from "@/components/base/BaseBreadcrumb.vue"
import BaseSvgIcon from "@/components/base/BaseSvgIcon.vue"
import BaseButton from "@/components/base/BaseButton.vue"

import addIcon from "@/assets/svg-icons/add.svg?raw"
import removeIcon from "@/assets/svg-icons/remove.svg?raw"
import closeIcon from "@/assets/svg-icons/close.svg?raw"

const cartStore = useCartStore()
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

    <table>
      <thead>
        <tr>
          <th>Produit</th>
          <th>Prix</th>
          <th>Quantité</th>
          <th>Total</th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in cartStore.cart" :key="item.product.id">
          <td>{{ item.product.name }}</td>
          <td>{{ item.product.price.toFixed(2) }} €</td>
          <td>
            <div class="quantity">
              {{ item.quantity }}
              <button class="add-button">
                <BaseSvgIcon :svg="addIcon" color="white" width="16px" />
              </button>
              <button class="remove-button">
                <BaseSvgIcon :svg="removeIcon" color="white" width="16px" />
              </button>
            </div>
          </td>
          <td>{{ (item.product.price * item.quantity).toFixed(2) }} €</td>
          <td>
            <button class="delete-button">
              <BaseSvgIcon :svg="closeIcon" color="white" width="16px" />
            </button>
          </td>
        </tr>
      </tbody>
    </table>

    <div class="summary-card">
      <h2>Total de votre panier</h2>
      <p class="summary-details">
        <span class="total-price">{{ cartStore.totalPrice.toFixed(2) }} €</span>
        ({{ cartStore.totalQuantity }} produits)
      </p>
      <BaseButton>Procéder au paiement</BaseButton>
    </div>

  </div>
</template>

<style scoped>
.content {
  margin-bottom: 100px;
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

.add-button,
.remove-button,
.delete-button {
  background-color: rgb(200, 200, 200);
  border-radius: 50%;
  padding: 2px;
}

.add-button,
.remove-button {
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

h2 {
  font-size: 16px;
  font-weight: 500;
}

.summary-details {
  margin-top: 10px;
  margin-bottom: 30px;
}

.total-price {
  font-weight: bold;
  color: var(--color-primary);
  margin-right: 5px;
}

@media (max-width: 600px) {
  .summary-card {
    display: flex;
    flex-direction: column;
    align-items: center;
  }
}
</style>