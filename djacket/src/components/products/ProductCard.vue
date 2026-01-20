<script setup lang="ts">
export type Product = {
  id: number
  categoryId: number
  name: string
  price: number
  thumbnail: string
}

const props = defineProps<{
  product: Product
}>()
</script>

<template>
  <div class="product-card">
    <img class="product-thumbnail" :src="props.product.thumbnail" :alt="props.product.name" />
    <div class="product-info">
      <div class="product-name">{{ props.product.name }}</div>
      <div class="product-price">{{ props.product.price }} €</div>
    </div>
  </div>
</template>

<style scoped>
.product-card {
  width: 300px;
  overflow: hidden;
  border-radius: 8px;
  background-color: white;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
  cursor: pointer;
}

.product-card:hover {
  background-color: var(--color-primary);
  outline: 2px solid var(--color-primary);
  color: white;
  box-shadow: none;
}

.product-thumbnail {
  width: 100%;
  height: auto;
}

.product-info {
  padding: 15px;
}

.product-name {
  font-size: 15px;
}

.product-price {
  font-size: 18px;
  font-weight: bold;
  margin-top: 10px;
  color: var(--color-primary);
}

.product-card:hover .product-price {
  color: white;
}

@media (max-width: 600px) {
  .product-card {
    width: 250px;
  }
}
</style>
