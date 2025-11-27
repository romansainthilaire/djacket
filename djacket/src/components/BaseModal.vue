<script setup lang="ts">
import { defineProps, defineEmits } from "vue"
import BaseButton from "./BaseButton.vue"

type Props = {
  title: string
  text: string
  width?: string
  showConfirmButton?: boolean
}

const {
  title,
  text,
  width = "450px",
  showConfirmButton = false
} = defineProps<Props>()

const emit = defineEmits<{
  (e: "close"): void
  (e: "confirm"): void
}>()

function close() {
  emit("close")
}

function confirm() {
  emit("confirm")
  close()
}
</script>

<template>
  <Teleport to="body">
    <div class="modal-overlay" @click="close()">
      <div class="modal" @click.stop>

        <div class="modal-header">
          <div class="modal-title">{{ title }}</div>
          <div class="modal-close">
            <button class="close-button" @click="close()">&times;</button>
          </div>
        </div>

        <div class="modal-body">
          <slot>
            {{ text }}
          </slot>
        </div>

        <div v-if="showConfirmButton" class="modal-footer">
          <BaseButton @click="confirm()">Confirmer</BaseButton>
        </div>

      </div>
    </div>
  </Teleport>
</template>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
}

.modal {
  background-color: white;
  border-radius: 8px;
  width: v-bind(width);
  max-width: 90%;
  overflow: hidden;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  padding: 20px;
  background-color: var(--color-primary-light);
}

.modal-title {
  font-size: 20px;
  font-weight: 600;
  color: var(--color-primary);
  padding-right: 20px;
}

.close-button {
  color: rgb(80, 80, 80);
  background: none;
  font-size: 30px;
  margin-right: -5px;
}

.modal-body {
  padding: 30px 20px;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  padding: 20px;
  border-top: 1px solid rgb(230, 230, 230);
}
</style>
