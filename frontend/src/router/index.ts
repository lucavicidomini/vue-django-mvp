import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'dashboard',
      component: () => import('../views/Dashboard.vue')
    },
    {
      path: '/vehicles',
      name: 'Vehicles',
      component: () => import('../views/VehicleList.vue')
    }
  ],
})

export default router
