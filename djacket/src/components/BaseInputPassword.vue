<script setup lang="ts">
import { ref, useTemplateRef, nextTick } from "vue"

type Props = {
  id: string
  label?: string
  required?: boolean
  errorMessage?: string
}

const {
  id,
  label = "",
  required = false,
  errorMessage = ""
} = defineProps<Props>()

const password = defineModel<string>({ required: true })

const showPassword = ref(false)
const outlineColor = ref("rgb(200, 200, 200)")
const inputRef = useTemplateRef<HTMLInputElement>("inputRef")

async function togglePasswordVisibility() {
  showPassword.value = !showPassword.value
  await nextTick()
  const input: HTMLInputElement = inputRef.value!
  input.focus()
  const length = input.value.length || 0
  input.setSelectionRange(length, length)
}
</script>

<template>
  <div class="form-field">
    <label v-if="label" :for="id">{{ label }}</label>
    <div class="input-container">
      <input
        ref="inputRef"
        :id="id"
        :type="showPassword ? 'text' : 'password'"
        :required="required"
        v-model="password"
        @focus="outlineColor = 'var(--color-primary)'"
        @blur="outlineColor = 'rgb(200, 200, 200)'"
      />
      <button type="button" @click.prevent="togglePasswordVisibility()">
        <img v-if="!showPassword" src="@/assets/svg-icons/eye.svg" alt="Montrer le mot de passe">
        <img v-else src="@/assets/svg-icons/eye-off.svg" alt="Cacher le mot de passe">
      </button>
    </div>
    <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
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
  display: flex;
  outline: 1px solid v-bind(outlineColor);
  border-radius: 4px;
}

input {
  width: 100%;
  box-sizing: border-box;
  padding: 10px;
  border: none;
  outline: none;
  color: var(--color-primary);
  font-size: 16px;
}

button {
  width: 50px;
  background-color: rgb(240, 240, 240);
}

button img {
  width: 28px;
}

.error-message {
  margin-top: 5px;
  font-size: 13px;
  color: var(--color-error);
}
</style>
