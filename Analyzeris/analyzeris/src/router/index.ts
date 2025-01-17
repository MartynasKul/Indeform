import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/login',
    component: () => import('../views/LoginView.vue')
  },
  {
    path: '/register',
    component: () => import('../views/RegisterView.vue')
  },
  {
    path: '/data',
    component: () => import('../views/DataView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/',
    redirect: '/data'
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router