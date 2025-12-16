import SignupView from "@/views/auth/SignupView.vue"
import VerifyEmailNoticeView from "@/views/auth/VerifyEmailNoticeView.vue"
import VerifyEmailView from "@/views/auth/VerifyEmailView.vue"
import ResendVerificationEmailView from "@/views/auth/ResendVerificationEmailView.vue"
import ResetPasswordView from "@/views/auth/ResetPasswordView.vue"
import ResetPasswordNoticeView from "@/views/auth/ResetPasswordNoticeView.vue"
import LoginView from "@/views/auth/LoginView.vue"


export default [
    {
      path: "/signup",
      name: "signup",
      component: SignupView,
      meta: { title: "Inscription" }
    },
    {
      path: "/verify-email-notice/:email",
      name: "verify-email-notice",
      component: VerifyEmailNoticeView,
      props: true,
      meta: { title: "Vérification de l'email" }
    },
    {
      path: "/verify-email",
      name: "verify-email",
      component: VerifyEmailView,
      meta: { title: "Vérification de l'email" }
    },
    {
      path: "/resend-verification-email",
      name: "resend-verification-email",
      component: ResendVerificationEmailView,
      meta: { title: "Vérification de l'email" }
    },
    {
      path: "/reset-password",
      name: "reset-password",
      component: ResetPasswordView,
      meta: { title: "Mot de passe oublié" }
    },
    {
      path: "/reset-password-notice/:email",
      name: "reset-password-notice",
      component: ResetPasswordNoticeView,
      props: true,
      meta: { title: "Réinitialisation du mot de passe" }
    },
    {
      path: "/login",
      name: "login",
      component: LoginView,
      meta: { title: "Connexion" }
    }
]
