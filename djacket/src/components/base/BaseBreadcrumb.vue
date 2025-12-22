<script setup lang="ts">
import BaseSvgIcon from "./BaseSvgIcon.vue"

import arrowForwardIcon from "@/assets/svg-icons/arrow-forward.svg?raw"


type BreadcrumbItem = {
  title: string,
  to?: string
}

const props = defineProps<{
  items: BreadcrumbItem[]
}>()
</script>

<template>
  <div class="breadcrumb">
    <span class="breadcrumb-item" v-for="(item, index) in props.items" :key="index">
      <RouterLink v-if="item.to" :to="item.to">{{ item.title }}</RouterLink>
      <span v-else>{{ item.title }}</span>
      <BaseSvgIcon
        class="separator"
        v-if="index != props.items.length - 1"
        :svg="arrowForwardIcon"
        color="rgb(100, 100, 100)"
        height="10px"
      />
    </span>
  </div>
</template>

<style scoped>
.breadcrumb {
  margin: 10px 0;
}

.breadcrumb-item {
  font-size: 13px;
  color: rgb(100, 100, 100);
}

.separator {
  margin: 0 5px;
}
</style>
