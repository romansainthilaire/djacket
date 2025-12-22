<script setup lang="ts">
const props = defineProps<{
  svg: string,
  color?: string,
  width?: string,
  height?: string
}>()
</script>

<template>
  <span class="svg-icon" v-html="props.svg"></span>
</template>

<style scoped>
.svg-icon {
  line-height: 0;
}

.svg-icon :deep(svg) {
  fill: v-bind(color);
  width: v-bind(width);
  height: v-bind(height);
}
</style>
