<script setup lang="ts">
import { ref } from 'vue'
import { MAppLayout, MContainer, MNavigationRail, MIconButton, type NavRailItem } from '@m3ui-vue/m3ui-vue'
import { RouterView } from 'vue-router';

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
const expanded = ref(false)
</script>

<template>
  <MAppLayout>
    <template #drawer>
      <MNavigationRail
        :items="items"
        :expanded="expanded"
        v-model="active"
      >
          <template #fab>
            <MIconButton
              :icon="expanded ? 'left_panel_close' : 'left_panel_open'"
              :label="expanded ? 'Collapse' : 'Expand'"
              @click="expanded = !expanded"
            />
          </template>
      </MNavigationRail>
    </template>
    <MContainer>
      <RouterView />
    </MContainer>
  </MAppLayout>
</template>

<style scoped></style>
