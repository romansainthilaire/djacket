<script setup lang="ts">
import BaseSvgIcon from "./BaseSvgIcon.vue"
import closeIcon from "@/assets/svg-icons/close.svg?raw"


type Props = {
  id: string
  type: "text" | "email"
  label?: string
  required?: boolean
  disabled?: boolean
  errorMessage?: string
  helpText?: string
  placeholder?: string
  showClearButton?: boolean
}

const {
  id,
  type,
  label = "",
  required = false,
  disabled = false,
  errorMessage = "",
  helpText = "",
  placeholder = "",
  showClearButton = false
} = defineProps<Props>()

const value = defineModel<string>({ required: true })
</script>

<template>
  <div class="form-field">
    <label v-if="label" :for="id">{{ label }}</label>
    <div class="input-container">
      <input
        :id="id"
        :type="type"
        :required="required"
        :disabled="disabled"
        :placeholder="placeholder"
        v-model="value"
      />
      <button
        v-if="showClearButton && value && !disabled"
        class="clear-button"
        @click="value = ''"
      >
        <BaseSvgIcon :svg="closeIcon" height="22px" color="var(--color-primary)" />
      </button>
    </div>
    <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
    <p v-else-if="helpText" class="help-text">{{ helpText }}</p>
  </div>
</template>

<style scoped>
.form-field {
  display: flex;
  flex-direction: column;
  margin-top: 20px;
}

label {
  margin-bottom: 5px;
  font-size: 16px;
}

.input-container {
  position: relative;
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

.clear-button {
  position: absolute;
  right: 5px;
  top: 9px;
  background: none;
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
