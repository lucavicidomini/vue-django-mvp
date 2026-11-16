import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'dashboard',
      component: () => import('../views/dashboard/Dashboard.vue')
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
    },
    {
      path: '/fuels',
      name: 'Fuels',
      component: () => import('../views/fuels/ListFuels.vue')
    },
  ],
})

export default router
