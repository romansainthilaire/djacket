import { createRouter, createWebHistory } from "vue-router"
import { useAuthStore } from "@/stores/auth"

import HomeView from "../views/HomeView.vue"
import SignupView from "../views/SignupView.vue"
import AboutView from "../views/AboutView.vue"

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "home",
      component: HomeView
    },
    {
      path: "/signup",
      name: "signup",
      component: SignupView
    },
    {
      path: "/about",
      name: "about",
      component: AboutView,
      meta: { loginRequired: true }
    }
  ]
})

router.beforeEach(async (to, from, next) => {
  const auth = useAuthStore()
  if (!auth.user) {
    await auth.setUser()
  }
  if (!auth.user && to.meta.loginRequired) {
    // TODO: user should be sent back to their original destination (redirect)
    return next("/")
  }
  next()
})

export default router
