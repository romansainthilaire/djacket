<script setup lang="ts">
import { ref,computed, onMounted } from "vue"
import api from "@/plugins/axios"

import type { Product } from "@/components/products/ProductCard.vue"
import BaseInputText from "@/components/base/BaseInputText.vue"
import ProductGrid from "@/components/products/ProductGrid.vue"
import BaseLoadingSpinner from "@/components/base/BaseLoadingSpinner.vue"


const products = ref<Product[]>([])
const search = ref("")

const filteredProducts = computed(() => {
  if (!search.value.trim()) {
    return products.value
  }
  const searchTerms = search.value.toLowerCase().split(" ").filter(Boolean)
  return products.value.filter(product => {
    const productName = product.name.toLowerCase()
    return searchTerms.some(term => productName.includes(term))
  })
})

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

    <div class="search-container">
      <BaseInputText
        type="text"
        v-model="search"
        placeholder="Rechercher une veste"
        show-clear-button
      />
    </div>

    <h3>
      <template v-if="search">Produits trouvés ({{ filteredProducts.length }})</template>
      <template v-else>Tous les produits ({{ products.length }})</template>
    </h3>

    <template v-if="products.length">
      <ProductGrid v-if="filteredProducts.length" :products="filteredProducts" />
      <p v-else class="no-results">Aucun produit ne correspond à votre recherche.</p>
    </template>

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

.search-container {
  max-width: 400px;
  margin: auto;
  margin-top: 60px;
}

h3 {
  font-size: 30px;
  font-weight: 500;
  text-align: center;
  margin: 50px 0;
  color: var(--color-primary);
}

.no-results {
  text-align: center;
  color: rgb(100, 100, 100);
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
