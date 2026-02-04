<script setup lang="ts">
import { ref, onMounted, watch } from "vue"
import api from "@/plugins/axios"

import type { Product } from "@/components/products/ProductCard.vue"
import BaseBreadcrumb from "@/components/base/BaseBreadcrumb.vue"
import ProductGrid from "@/components/products/ProductGrid.vue"
import BaseLoadingSpinner from "@/components/base/BaseLoadingSpinner.vue"

export type Category = {
  name: string,
  slug: string
}

const props = defineProps<{
  categorySlug: string
}>()

const category = ref<Category | null>(null)
const products = ref<Product[]>([])

async function fetchCategory() {
  const response = await api.get(`categories/${props.categorySlug}/`)
  category.value = response.data
}

async function fetchProducts() {
  const response = await api.get(`products?category=${props.categorySlug}`)
  products.value = response.data
}

onMounted(async () => {
  await fetchCategory()
  await fetchProducts()
  document.title = `Djacket - ${category.value!.name}`
})

watch(() => props.categorySlug, async () => {
  category.value = null
  products.value = []
  await fetchCategory()
  await fetchProducts()
  document.title = `Djacket - ${category.value!.name}`
})
</script>

<template>
  <div class="content">

    <template v-if="category && products.length">
      <BaseBreadcrumb
        :items="[
          { title: 'Accueil', to: '/' },
          { title: category.name }
        ]"
      />
      <h1>Collection {{ category.name }}</h1>
      <ProductGrid class="products" :products="products" />
    </template>
    
    <div v-else class="loading-container">
      <BaseLoadingSpinner />
      <div class="loading-text">Chargement...</div>
    </div>

  </div>
</template>

<style scoped>
.content {
  padding-bottom: 100px;
}

h1 {
  font-size: 30px;
  font-weight: 500;
  text-align: center;
  margin-top: 40px;
  margin-bottom: 60px;
  color: var(--color-primary);
}

.loading-container {
  margin-top: 50px;
  text-align: center;
}

@media (max-width: 600px) {
  .content {
    padding-bottom: 80px;
  }

  h1 {
    font-size: 20px;
    margin-top: 30px;
    margin-bottom: 40px;
  }
}
</style>
