import { defineStore } from "pinia"
import { ref, computed } from "vue"

type Item = {
  productId: number
  quantity: number
}

export const useCartStore = defineStore("cart", () => {

  const cart = ref<Item[]>(
    localStorage.getItem("cart")
    ? JSON.parse(localStorage.getItem("cart")!)
    : []
  )

  const totalQuantity = computed((): number => {
    let totalQuantity = 0
    cart.value.forEach(item => {
      totalQuantity += item.quantity
    })
    return totalQuantity
  })

  function addToCart(item: Item) {
    const existingItem = cart.value.find(i => i.productId == item.productId)
    if (existingItem) {
      existingItem.quantity += item.quantity
    } else {
      cart.value.push(item)
    }
    localStorage.setItem("cart", JSON.stringify(cart.value))
  }

  return {
    cart,
    totalQuantity,
    addToCart
  }
})
