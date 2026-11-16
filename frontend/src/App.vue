<script setup lang="ts">
import { ref } from 'vue'
import { MFab, type NavRailItem, MNavigationSuite } from '@m3ui-vue/m3ui-vue'
import { RouterView } from 'vue-router';
import { useFabStore } from '@/stores/fab'
const items: NavRailItem[] = [
  {
    label: 'Dashboard',
    icon: 'dashboard',
    value: 'dashboard',
    to: '/'
  },
  {
    label: 'Vehicles',
    icon: 'directions_car',
    value: 'vehicles',
    to: '/vehicles'
  },
]

const active = ref(items[0]!.value)

const fab = useFabStore()
const onFabClick = () => fab.action?.()
</script>

<template>
  <MNavigationSuite
    v-model="active"
    :items="items"
    class="h-dvh"
  >
    <main class="p-4">
      <RouterView />
    </main>

    <template #fab v-if="fab.isVisible">
      <MFab
        :icon="fab.icon"
        @click="onFabClick"
      />
    </template>
  </MNavigationSuite>
</template>

<style scoped></style>
