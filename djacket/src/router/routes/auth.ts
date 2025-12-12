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
      path: "/reset-password",
      name: "reset-password",
      component: ResetPasswordView
    },
    {
      path: "/reset-password-notice/:email",
      name: "reset-password-notice",
      component: ResetPasswordNoticeView,
      props: true
    },
    {
      path: "/login",
      name: "login",
      component: LoginView
    }
]
