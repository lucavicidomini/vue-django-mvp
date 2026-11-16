<script setup lang="ts">
import { type VehicleRechargeSpeed } from '@/stores/vehicle';
import {  MButton, MSection, MTextField, MList, MListItem, MDialog, MGrid } from '@m3ui-vue/m3ui-vue';
import { computed, reactive, ref, type PropType } from 'vue';

const props = defineProps({
  recharge_speeds: {
    type: Array as PropType<VehicleRechargeSpeed[]>,
    required: false,
  },
});

interface Item extends VehicleRechargeSpeed {
    _key: number;
}

const emit = defineEmits(['update'])
const rechargeSpeeds = (props.recharge_speeds ?? [] as VehicleRechargeSpeed[]).map((rechargeSpeed, i) => ({ ...rechargeSpeed, _key: i }))
const rows = reactive<Item[]>([ ... rechargeSpeeds ])

const emptyItem: () => Item = () => ({ _key: rows.length, id: 0, name: '', gross_speed: 0, net_speed: 0 })
const selectedItem = ref<Item | null>(null)
const editItem = (scenario: Item) => selectedItem.value = ({ ...scenario })
const saveSelectedItem = () => {
  const scenario = selectedItem.value as Item;
  if (selectedItem.value) {
    const index = rows.findIndex(r => r._key === scenario!._key)
    if (index !== -1) {
      rows[index] = { ...scenario }
    } else {
      rows.push({ ...scenario })
    }
    selectedItem.value = null
    emit('update', [...rows])
  }
}
const deleteSelectedItem = () => {
  if (selectedItem.value) {
    const index = rows.findIndex(r => r._key === selectedItem.value!._key)
    if (index !== -1) {
      rows.splice(index, 1)
    }
    selectedItem.value = null
    emit('update', [...rows])
  }
}

const open = computed(() => !!selectedItem.value)

</script>

<template>
  <MDialog v-model="open" title="Recharge speed" :closable="false">
    <MGrid v-if="selectedItem" class="gap-4" :cols="2" :sm="1">
      <MTextField v-model="selectedItem.name" required label="Name" />
      <MTextField v-model="selectedItem.gross_speed" required label="Gross Speed" />
      <MTextField v-model="selectedItem.net_speed" required label="Net Speed" />
    </MGrid>
    <template #actions>
      <MButton variant="text" @click="selectedItem = null">Cancel</MButton>
      <MButton variant="text" color="error" @click="deleteSelectedItem()">Delete</MButton>
      <MButton variant="text" @click="saveSelectedItem()">Save</MButton>
    </template>
  </MDialog>

  <MSection
    gap="none"
    title="Recharge speeds"
  >
    <template #actions>
      <MButton variant="text" size="sm" @click="selectedItem = emptyItem()">Add recharge speed</MButton>
    </template>

    <MList segmented>
      <MListItem
        v-for="scenario in rows"
        :key="scenario._key"
        :title="scenario.name"
        :subtitle="scenario.net_speed?.toString()"
        @click="editItem(scenario)"
        class="bg-surface-container-lowest"
      ></MListItem>
    </MList>
  </MSection>
  
</template>

<style scoped></style>
