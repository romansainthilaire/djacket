<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount, useTemplateRef } from "vue"


type DropdownLink = {
  text: string,
  to: string
}

type Props = {
  name: string,
  links: DropdownLink[],
  menuWidth?: string
}

const {
  name,
  links,
  menuWidth = "150px"
} = defineProps<Props>()

const isOpen = ref(false)
const dropdownMenuRef = useTemplateRef<HTMLElement>("dropdownMenuRef")

onMounted(() => {
  document.addEventListener("click", onClickOutside)
})

onBeforeUnmount(() => {
  document.removeEventListener("click", onClickOutside)
})

function onClickOutside(event: MouseEvent) {
  const target = event.target as Node
  if (!dropdownMenuRef.value?.contains(target)) {
    isOpen.value = false
  }
}
</script>

<template>
  <div class="dropdown">

    <button
      class="dropdown-button"
      :class="{'is-open': isOpen}"
      @click.stop="isOpen = !isOpen"
    >
      {{ name }}
    </button>

    <div v-if="isOpen" ref="dropdownMenuRef" class="dropdown-menu">
      <RouterLink
        class="dropdown-link"
        v-for="link in links"
        :key="link.to"
        :to="link.to"
        @click="isOpen = false"
      >
        {{ link.text }}
      </RouterLink>
    </div>

  </div>
</template>

<style scoped>
.dropdown {
  position: relative;
  display: inline-block;
}

.dropdown-button {
  color: white;
  font-size: 16px;
  line-height: initial;
  padding: 6px 12px;
  background-color: transparent;
  border-radius: 4px;
  margin: 0 5px;
  transition: background-color 0.3s ease;
}

.dropdown-button:hover,
.dropdown-button.is-open {
  background-color: rgba(255, 255, 255, 0.15);
}

.dropdown-menu {
  position: absolute;
  top: 40px;
  left: 5px;
  width: v-bind(menuWidth);
  background-color: white;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
  z-index: 1000;
  border-radius: 4px;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.dropdown-link {
  padding: 10px 12px;
  color: var(--color-primary);
  text-decoration: none;
  transition: background-color 0.3s ease;
}

.dropdown-link:hover {
  background-color: var(--color-primary-light);
}

@media (max-width: 600px) {
  .dropdown-button {
    margin: 8px 0;
    padding: 0;
  }

  .dropdown-button:hover {
    background-color: transparent;
  }

  .dropdown-button.is-open {
    background-color: transparent;
    text-decoration: underline;
    text-underline-offset: 4px;
  }

  .dropdown-menu {
    left: 0;
  }
}
</style>
