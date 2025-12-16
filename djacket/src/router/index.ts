import { createRouter, createWebHistory } from "vue-router"
import { useUserStore } from "@/stores/user"

import authRoutes from "./routes/auth"
import userRoutes from "./routes/user"

import NotFoundView from "../views/NotFoundView.vue"
import HomeView from "../views/HomeView.vue"


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
