<script setup lang="ts">
import { ref, onMounted } from "vue"
import api from "@/plugins/axios"

import type { Product } from "@/components/products/ProductCard.vue"
import ProductGrid from "@/components/products/ProductGrid.vue"
import BaseLoadingSpinner from "@/components/base/BaseLoadingSpinner.vue"


const products = ref<Product[]>([])

onMounted(async () => {
  const response = await api.get("products/")
  products.value = response.data
})
</script>

<template>
  <div class="content">

    <div class="header">
      <h1>Bienvenue sur <span class="brand">Djacket</span></h1>
      <h2>Le meilleur endroit pour trouver votre veste idéale.</h2>
    </div>

    <h3>Tous les produits</h3>

    <ProductGrid v-if="products.length" :products="products" />

    <BaseLoadingSpinner v-else text="Chargement..." />

  </div>
</template>

<style scoped>
.content {
  padding-top: 80px;
  padding-bottom: 100px;
}

.header {
  margin: auto;
  width: fit-content;
  text-align: center;
  border: 2px solid var(--color-primary);
  border-radius: 15px;
  color: rgb(80, 80, 80);
  padding: 50px;
}

.brand {
  font-family: "Fjalla One", sans-serif;
  font-weight: bold;
  color: var(--color-primary);
}

h1 {
  font-size: 40px;
  font-weight: 500;
}

h2 {
  font-size: 18px;
  font-weight: normal;
  margin-top: 15px;
}

h3 {
  font-size: 30px;
  font-weight: 500;
  text-align: center;
  margin-top: 80px;
  margin-bottom: 50px;
  color: var(--color-primary);
}

@media (max-width: 600px) {
  .content {
    padding-top: 40px;
    padding-bottom: 80px;
  }

  .header {
    border: none;
    padding: 0;
  }

  h1 {
    font-size: 25px;
  }

  h2 {
    font-size: 15px;
    margin-top: 10px;
  }

  h3 {
    font-size: 20px;
    margin: 40px 0;
  }
}
</style>
