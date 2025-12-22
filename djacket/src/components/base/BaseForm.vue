<script setup lang="ts">
type Props = {
  title: string
  maxWidth?: string
}

const {
  title,
  maxWidth = "450px"
} = defineProps<Props>()

const emit = defineEmits<{
  (e: "submit"): void
}>()
</script>

<template>
  <div class="content">
    <div class="card">

      <div class="header">
        <h1>{{ title }}</h1>
      </div>

      <form @submit.prevent="emit('submit')">
        <slot></slot>
      </form>

    </div>
  </div>
</template>

<style scoped>
.content {
  display: flex;
  justify-content: center;
  padding-top: 60px;
  padding-bottom: 100px;
}

.card {
  width: 100%;
  max-width: v-bind(maxWidth);
  border-radius: 8px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
}

.header {
  height: 100px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: var(--color-primary-light);
}

h1 {
  color: var(--color-primary);
  font-size: 25px;
  font-weight: 600;
}

form {
  padding: 0 30px;
}

@media (max-width: 600px) {
  .content {
    padding-top: 0;
    padding-bottom: 50px;
  }

  .card {
    max-width: none;
    border-radius: 0;
    box-shadow: none;
  }

  .header {
    margin-left: -20px;
    margin-right: -20px;
    padding: 0 20px;
  }

  form {
    padding: 0;
  }
}
</style>
