<script setup lang="ts">
import { useId } from "vue"

type Props = {
  label: string
  disabled?: boolean
}

const {
  label,
  disabled = false
} = defineProps<Props>()

const id = useId()
const value = defineModel<boolean>()
</script>

<template>
  <div class="input-container">
    <input
      type="checkbox"
      v-model="value"
      :id="id"
      :disabled="disabled"
    />
    <label :for="id">{{ label }}</label>
  </div>
</template>

<style scoped>
.input-container {
  display: flex;
  align-items: center;
  gap: 5px;
}

input {
  accent-color: var(--color-primary);
  width: 16px;
  height: 16px;
  cursor: pointer;
}

input:disabled {
  cursor: initial;
}

label {
  color: rgb(80, 80, 80);
  font-size: 14px;
}
</style>
