<script setup lang="ts">
import { computed } from "vue"
import BaseInputPassword from "@/components/base/BaseInputPassword.vue"

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

const passwordValidationRules = computed((): Array<{ text: string, checked: boolean }> => [
  { text: "Au moins 8 caractères", checked: password.value.length >= 8 },
  { text: "Une lettre majuscule", checked: /[A-Z]/.test(password.value) },
  { text: "Une lettre minuscule", checked: /[a-z]/.test(password.value) },
  { text: "Un chiffre", checked: /\d/.test(password.value) },
  { text: "Un caractère spécial (!@#$%^&* etc.)", checked: /[!@#$%^&*(),.?":{}|<>]/.test(password.value) }
])

const passwordIsValid = computed(() =>
  passwordValidationRules.value.every(rule => rule.checked)
)

defineExpose({
  passwordIsValid
})
</script>

<template>

  <BaseInputPassword
    v-model="password"
    :id="id"
    :label="label"
    :required="required"
    :error-message="errorMessage"
  />

  <div class="password-validation-rules">
    Doit inclure :
    <ul>
      <li
        v-for="rule in passwordValidationRules"
        :key="rule.text"
        :class="{ 'checked': rule.checked }"
      >
        <span>{{ rule.text }}</span>
      </li>
    </ul>
  </div>

</template>

<style scoped>
.password-validation-rules {
  margin-top: 10px;
  font-size: 13px;
  color: rgb(100, 100, 100);
}

.password-validation-rules ul {
  list-style: none;
  margin-top: 5px;
}

.password-validation-rules li {
  position: relative;
  padding-left: 20px;
}

.password-validation-rules li::before {
  content: "•";
  position: absolute;
  left: 0;
  width: 15px;
  text-align: center;
}

.password-validation-rules li.checked::before {
  content: "✔";
  color: var(--color-success);
}
</style>
