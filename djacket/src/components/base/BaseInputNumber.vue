<script setup lang="ts">
import { useId } from "vue"

type Props = {
  label?: string
  required?: boolean
  disabled?: boolean
  errorMessage?: string
  helpText?: string
  placeholder?: string
  min?: number
  max?: number
  step?: number
}

const {
  label = "",
  required = false,
  disabled = false,
  errorMessage = "",
  helpText = "",
  placeholder = "",
  min,
  max,
  step
} = defineProps<Props>()

const id = useId()
const value = defineModel<number | null>({ required: true })

function onInput(event: Event) {
  const raw = (event.target as HTMLInputElement).value
  if (raw == "") {
    value.value = null
    return
  }
  const parsed = Number(raw)
  if (isNaN(parsed)) {
    return
  }
  value.value = parsed
}
</script>

<template>
  <div class="form-field">
    <label v-if="label" :for="id">{{ label }}</label>
    <input
      type="number"
      :id="id"
      :required="required"
      :disabled="disabled"
      :placeholder="placeholder"
      :min="min"
      :max="max"
      :step="step"
      :value="value ?? ''"
      @input="onInput"
    />
    <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
    <p v-else-if="helpText" class="help-text">{{ helpText }}</p>
  </div>
</template>

<style scoped>
.form-field {
  display: flex;
  flex-direction: column;
}

label {
  margin-bottom: 5px;
  font-size: 16px;
}

input {
  width: 100%;
  box-sizing: border-box;
  padding: 10px;
  border: none;
  border-radius: 4px;
  outline: 1px solid rgb(200, 200, 200);
  color: var(--color-primary);
  font-size: 16px;
}

input:focus {
  outline: 1px solid var(--color-primary);
}

input::placeholder {
  color: rgb(150, 150, 150);
}

.error-message {
  margin-top: 5px;
  font-size: 13px;
  color: var(--color-error);
}

.help-text {
  margin-top: 5px;
  font-size: 13px;
  color: rgb(100, 100, 100);
}
</style>
