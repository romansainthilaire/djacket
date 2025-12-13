<script setup lang="ts">
import { computed } from "vue"

type Props = {
  type?: "button" | "submit" | "reset"
  size?: "small" | "medium" | "large"
  disabled?: boolean
  color?: string
  bgColor?: string
  bgColorHover?: string
}

const {
  type = "button",
  size = "medium",
  disabled = false,
  color = "white",
  bgColor = "var(--color-primary)",
  bgColorHover = "var(--color-primary)"
} = defineProps<Props>()

const sizeStyle = computed(() => {
  switch (size) {
    case "small":
      return {
        height: "30px",
        padding: "0 14px",
        fontSize: "14px"
      }
    case "medium":
      return {
        height: "35px",
        padding: "0 16px",
        fontSize: "16px"
      }
    case "large":
      return {
        height: "40px",
        padding: "0 18px",
        fontSize: "18px"
      }
  }
})
</script>

<template>
  <button :type="type" :disabled="disabled" :style="sizeStyle">
    <slot></slot>
  </button>
</template>

<style scoped>
button {
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 4px;
  background-color: v-bind(bgColor);
  color: v-bind(color);
  transition: background-color 0.3s ease;
}

button:hover {
  background-color: v-bind(bgColorHover);
}

button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
</style>
