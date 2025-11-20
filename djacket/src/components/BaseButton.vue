<script setup lang="ts">
type Props = {
  type?: "button" | "submit" | "reset"
  disabled?: boolean
  color?: string
  bgColor?: string
  hoverBgColor?: string
}

const {
  type = "button",
  disabled = false,
  color = "white",
  bgColor = "rgb(0, 0, 140)",
  hoverBgColor = "rgb(0, 0, 140)"
} = defineProps<Props>()
</script>

<template>
  <button :type="type" :disabled="disabled">
    <slot></slot>
  </button>
</template>

<style scoped>
button {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0 16px;
  height: 35px;
  border-radius: 4px;
  background-color: v-bind(bgColor);
  color: v-bind(color);
  font-size: 16px;
  transition: background-color 0.3s ease;
}

button:hover {
  background-color: v-bind(hoverBgColor);
}

button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
</style>