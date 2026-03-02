<script setup lang="ts">
import { useCartStore } from "@/stores/cart"

const cartStore = useCartStore()
</script>

<template>

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
          {{ item.quantity }}
          <button>+</button>
          <button>-</button>
        </td>
        <td>{{ (item.product.price * item.quantity).toFixed(2) }} €</td>
        <td>
          <button>Retirer</button>
        </td>
      </tr>
    </tbody>
  </table>

  <h2>Total de votre panier</h2>

  <p>{{ cartStore.totalQuantity }} produits</p>
  <p>{{ cartStore.totalPrice.toFixed(2) }} €</p>

</template>

<style scoped>
table {
  width: 100%;
  border-radius: 8px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
  padding: 15px;
}
</style>