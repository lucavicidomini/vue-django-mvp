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
      component: () => import('../views/vehicles/ListVehicles.vue')
    },
    {
      path: '/vehicles/new',
      name: 'Vehicles-new',
      component: () => import('../views/vehicles/CreateVehicle.vue')
    },
    {
      path: '/vehicles/:id',
      name: 'Vehicles-edit',
      component: () => import('../views/vehicles/EditVehicle.vue')
    }
  ],
})

export default router
