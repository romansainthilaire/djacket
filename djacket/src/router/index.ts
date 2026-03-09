import { createRouter, createWebHistory } from "vue-router"
import { useUserStore } from "@/stores/user"

import authRoutes from "./routes/auth"
import userRoutes from "./routes/user"

import NotFoundView from "../views/NotFoundView.vue"
import HomeView from "../views/HomeView.vue"
import CategoryDetailView from "../views/CategoryDetailView.vue"
import ProductDetailView from "../views/ProductDetailView.vue"
import CartView from "../views/CartView.vue"
import PaymentView from "../views/PaymentView.vue"


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "home",
      component: HomeView
    },
    ...authRoutes,
    ...userRoutes,
    {
      path: "/:categorySlug",
      name: "category-detail",
      component: CategoryDetailView,
      props: true
    },
    {
      path: "/:categorySlug/:productId",
      name: "product-detail",
      component: ProductDetailView,
      props: route => ({ productId: Number(route.params.productId) })
    },
    {
      path: "/cart",
      name: "cart",
      component: CartView,
      meta: { title: "Panier" }
    },
    {
      path: "/cart/payment",
      name: "payment",
      component: PaymentView,
      meta: {
        title: "Paiement",
        loginRequired: true
      }
    },
    {
      path: "/:pathMatch(.*)*",
      name: "not-found",
      component: NotFoundView ,
      meta: { title: "Page non trouvée" }
    }
  ]
})

router.beforeEach(async (to, from, next) => {
  const appName = "Djacket"
  document.title = to.meta.title ? `${appName} - ${to.meta.title}` : appName
  const userStore = useUserStore()
  if (!userStore.user) {
    await userStore.fetchUser()
  }
  if (!userStore.user && to.meta.loginRequired) {
    return next("/login")
  }
  next()
})

export default router
