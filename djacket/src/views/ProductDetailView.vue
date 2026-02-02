<script setup lang="ts">
import { ref, computed, onMounted } from "vue"
import api from "@/plugins/axios"
import { useCartStore } from "@/stores/cart"

import BaseBreadcrumb from "@/components/base/BaseBreadcrumb.vue"
import BaseLoadingSpinner from "@/components/base/BaseLoadingSpinner.vue"

type Product = {
  id: number,
  category: {
    name: string,
    slug: string
  }
  name: string,
  description: string,
  price: string,
  image: string
}

const props = defineProps<{
  productId: number
}>()

const cartStore = useCartStore()

const product = ref<Product | null>(null)
const quantity = ref(1)

const isValidQuantity = computed(() => {
  return Number.isInteger(quantity.value) && quantity.value >= 1
})

onMounted(async () => {
  const response = await api.get(`products/${props.productId}/`)
  product.value = response.data
  document.title = `Djacket - ${product.value?.name}`
})

function addToCart() {
  if (!isValidQuantity.value) {
    return
  }
  cartStore.addToCart({
    productId: props.productId,
    quantity: quantity.value
  })
}
</script>

<template>
  <div class="content">

    <template v-if="product">
      <BaseBreadcrumb
        class="breadcrumb"
        :items="[
          { title: product.category.name, to: `/${product.category.slug}` },
          { title: product.name }
        ]"
      />
      <div class="product-detail">
        <div class="product-info">
          <img class="product-image" :src="product.image" :alt="product.name">
          <h1 class="product-name">{{ product.name }}</h1>
          <p class="product-description">{{ product.description }}</p>
        </div>
        <div class="product-purchase">
          <h2 class="product-price">Prix : <span class="product-price-value">{{ product.price }} €</span></h2>
          <div class="add-to-cart-container">
            <input class="quantity-input" type="number" min="1" step="1" v-model="quantity">
            <button
              class="add-to-cart-button" 
              @click="addToCart()"
              :disabled="!isValidQuantity"
            >
              Ajouter au panier
            </button>
          </div>
        </div>
      </div>
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

.breadcrumb {
  width: 100%;
  text-align: left;
  margin-bottom: 40px;
}

.product-detail {
  display: flex;
  gap: 50px;
}

.product-info {
  max-width: 600px;
}

.product-image {
  width: 100%;
}

.product-name {
  margin-top: 20px;
  color: var(--color-primary);
  font-size: 30px;
}

.product-description {
  margin-top: 15px;
  white-space: pre-line;
  text-align: justify;
}

.product-price {
  font-weight: normal;
}

.product-price-value {
  font-weight: bold;
  color: var(--color-primary);
}

.add-to-cart-container {
  margin-top: 30px;
  display: flex;
  align-items: center;
}

.quantity-input {
  height: 40px;
  width: 80px;
  box-sizing: border-box;
  padding: 0 10px;
  border: none;
  border-top-left-radius: 4px;
  border-bottom-left-radius: 4px;
  outline: 1px solid rgb(200, 200, 200);
  color: var(--color-primary);
  font-size: 18px;
}

.quantity-input:focus {
  outline: 1px solid var(--color-primary);
}

.add-to-cart-button {
  height: 40px;
  border: none;
  outline: 1px solid var(--color-primary);
  padding: 0 15px;
  border-top-right-radius: 4px;
  border-bottom-right-radius: 4px;
  background-color: var(--color-primary);
  color: white;
  font-size: 16px;
  cursor: pointer;
}

.add-to-cart-button:disabled {
  cursor: not-allowed;
}

.loading-container {
  margin-top: 50px;
  text-align: center;
}

@media (max-width: 1100px) {
  .content {
    display: flex;
    flex-direction: column;
    align-items: center;
  }

  .product-detail {
    display: block;
  }

  .product-info {
    max-width: 500px;
  }

  .product-purchase {
    margin-top: 40px;
  }
}

@media (max-width: 600px) {
  .content {
    padding-bottom: 80px;
  }

  .breadcrumb {
    margin-bottom: 30px;
  }

  .product-info {
    max-width: 100%;
  }

  .product-name {
    font-size: 25px;
  }

  .product-price {
    font-size: 20px;
  }
}
</style>
