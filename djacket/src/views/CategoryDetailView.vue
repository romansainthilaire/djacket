<script setup lang="ts">
import { ref, computed, onMounted, watch } from "vue"
import api from "@/plugins/axios"
import { useRouter } from "vue-router"

import type { Product } from "@/components/products/ProductCard.vue"
import BaseBreadcrumb from "@/components/base/BaseBreadcrumb.vue"
import BaseInputText from "@/components/base/BaseInputText.vue"
import ProductGrid from "@/components/products/ProductGrid.vue"
import BaseLoadingSpinner from "@/components/base/BaseLoadingSpinner.vue"


const props = defineProps<{
  categorySlug: string
}>()

const router = useRouter()

const products = ref<Product[]>([])

const category = computed(() => {
  return products.value[0]!.category
})

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

async function fetchProducts() {
  try {
    const response = await api.get(`products?category=${props.categorySlug}`)
    products.value = response.data
  } catch (error: any) {
    if (error.status == 404) {
      router.push({ name: "not-found" })
      return
    }
  }
  document.title = `Djacket - ${category.value?.name}`
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

      <p class="nb-products-found">
        {{ filteredProducts.length }}
        produit{{ filteredProducts.length > 1 ? "s" : "" }}
        trouvé{{ filteredProducts.length > 1 ? "s" : "" }}
      </p>

      <div class="search-container">
        <BaseInputText
          v-model="search"
          placeholder="Rechercher une veste"
          show-clear-button
        />
      </div>

      <ProductGrid class="products" :products="filteredProducts" />
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
  margin-bottom: 10px;
  color: var(--color-primary);
}

.nb-products-found {
  font-size: 16px;
  text-align: center;
  color: rgb(80, 80, 80);
}

.search-container {
  max-width: 400px;
  margin: auto;
  margin-top: 50px;
  margin-bottom: 60px;
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
  }

  .nb-products-found {
    font-size: 14px;
  }
}
</style>
