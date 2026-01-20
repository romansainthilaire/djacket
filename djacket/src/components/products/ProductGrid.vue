<script setup lang="ts">
import ProductCard, { type Product } from "./ProductCard.vue"

const props = defineProps<{
  products: Product[]
}>()
</script>

<template>
  <div class="product-grid">
    <ProductCard v-for="product in props.products" :key="product.id" :product="product" />
  </div>
</template>

<style scoped>
.product-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  justify-items: center;
  gap: 50px;
}

@media (min-width: 751px) and (max-width: 1100px) {
  .product-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .product-grid > *:nth-child(2n + 1) {
    justify-self: end;
  }

  .product-grid > *:nth-child(2n) {
    justify-self: start;
  }
}

@media (max-width: 750px) {
  .product-grid {
    grid-template-columns: repeat(1, 1fr);
  }
}
</style>
