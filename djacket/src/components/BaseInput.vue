<script setup lang="ts">
type Props = {
  id: string
  type: "text" | "email"
  label?: string
  required?: boolean
  errorMessage?: string
}

const {
  id,
  type = "text",
  label = "",
  required = false,
  errorMessage = ""
} = defineProps<Props>()

const value = defineModel<string>({ required: true })
</script>

<template>
  <div class="form-field">
    <label v-if="label" :for="id">{{ label }}</label>
    <input
      :id="id"
      :type="type"
      :required="required"
      v-model="value"
    />
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

.error-message {
  margin-top: 5px;
  font-size: 13px;
  color: var(--color-error);
}
</style>
