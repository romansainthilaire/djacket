import { defineStore } from "pinia"
import { ref, computed } from "vue"

type Item = {
  product: {
    id: number
    name: string
    price: number
  }
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

  const totalPrice = computed((): number => {
    let totalPrice = 0
    cart.value.forEach(item => {
      totalPrice += item.product.price * item.quantity
    })
    return totalPrice
  })

  function addToCart(item: Item) {
    const existingItem = cart.value.find(i => i.product.id == item.product.id)
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
    totalPrice,
    addToCart
  }
})
