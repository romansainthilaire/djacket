<script setup lang="ts">
import { ref, computed, onMounted, watch } from "vue"
import api from "@/plugins/axios"

import type { Product } from "@/components/products/ProductCard.vue"
import BaseBreadcrumb from "@/components/base/BaseBreadcrumb.vue"
import ProductGrid from "@/components/products/ProductGrid.vue"
import BaseLoadingSpinner from "@/components/base/BaseLoadingSpinner.vue"


const props = defineProps<{
  categorySlug: string
}>()

const products = ref<Product[]>([])

const category = computed(() => {
  return products.value[0]!.category
})

async function fetchProducts() {
  products.value = []
  const response = await api.get(`products?category=${props.categorySlug}`)
  products.value = response.data
  document.title = `Djacket - ${category.value!.name}`
}

onMounted(() => {
  fetchProducts()
})

watch(() => props.categorySlug, () => {
  fetchProducts()
})
</script>

<template>
  <div class="content">

    <template v-if="products.length">
      <BaseBreadcrumb
        :items="[
          { title: 'Accueil', to: '/' },
          { title: category.name }
        ]"
      />
      <h1>Collection {{ category.name }}</h1>
      <ProductGrid class="products" :products="products" />
    </template>
    
    <BaseLoadingSpinner v-else class="loading-spinner" text="Chargement..." />

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

.loading-spinner {
  margin-top: 50px;
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
