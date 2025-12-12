import UserAccountView from "@/views/user/UserAccountView.vue"
import ChangeUsernameView from "@/views/user/ChangeUsernameView.vue"
import ChangePasswordView from "@/views/user/ChangePasswordView.vue"


export default [
    {
      path: "/user-account",
      name: "user-account",
      component: UserAccountView,
      meta: { loginRequired: true }
    },
    {
      path: "/user-account/change-username",
      name: "change-username",
      component: ChangeUsernameView,
      meta: { loginRequired: true }
    },
    {
      path: "/user-account/change-password",
      name: "change-password",
      component: ChangePasswordView,
      meta: { loginRequired: true }
    }
]
