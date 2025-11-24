import { createRouter, createWebHistory } from "vue-router"
import { useAuthStore } from "@/stores/auth"

import HomeView from "../views/HomeView.vue"
import SignupView from "../views/SignupView.vue"
import VerifyEmailNoticeView from "../views/VerifyEmailNoticeView.vue"
import VerifyEmailView from "../views/VerifyEmailView.vue"
import ResendVerificationEmailView from "../views/ResendVerificationEmailView.vue"
import LoginView from "../views/LoginView.vue"

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
      path: "/verify-email-notice/:email",
      name: "verify-email-notice",
      component: VerifyEmailNoticeView,
      props: true
    },
    {
      path: "/verify-email",
      name: "verify-email",
      component: VerifyEmailView
    },
    {
      path: "/resend-verification-email",
      name: "resend-verification-email",
      component: ResendVerificationEmailView
    },
    {
      path: "/login",
      name: "login",
      component: LoginView
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
