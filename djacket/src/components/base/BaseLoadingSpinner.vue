<script setup lang="ts">
type Props = {
  size?: string
  text?: string
}

const {
  size = "60px",
  text = ""
} = defineProps<Props>()
</script>

<template>
  <div class="loading-container">
    <img
      src="@/assets/svg-icons/loading-spinner.svg"
      alt="Chargement"
      :style="{ 'width': size, 'height': size }"
    />
    <div class="loading-text" v-if="text">{{ text }}</div>
  </div>
</template>

<style scoped>
.loading-container {
  text-align: center;
}

.loading-text {
  margin-top: 5px;
}
</style>
