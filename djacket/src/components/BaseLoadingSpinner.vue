<script setup lang="ts">
type Props = { size?: string }

const { size = "60px" } = defineProps<Props>()
</script>

<template>
  <img
    src="@/assets/svg-icons/loading-spinner.svg"
    alt="Chargement"
    :style="{ 'width': size, 'height': size }"
  />
</template>
