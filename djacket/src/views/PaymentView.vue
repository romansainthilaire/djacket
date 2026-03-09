<script setup lang="ts">
import { useCartStore } from "@/stores/cart"

import BaseBreadcrumb from "@/components/base/BaseBreadcrumb.vue"

const cartStore = useCartStore()
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

    <h1>Paiement</h1>

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
      <h2>Total de votre panier</h2>
      <p class="summary-details">
        <span class="total-price">{{ cartStore.totalPrice.toFixed(2) }} €</span>
        ({{ cartStore.totalQuantity }} article{{ cartStore.totalQuantity > 1 ? "s" : "" }})
      </p>
    </div>

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

h2 {
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